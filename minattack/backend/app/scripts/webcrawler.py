import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import re
from collections import deque

from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.technologie import Technologie
from minattack.backend.app.models.utiliser import Utiliser

import logging

logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, base_url, max_depth=3, id_audit=None, id_domaine=None):
        self.base_url = base_url.rstrip('/')
        self.domaine_model = Domaine(url_domaine=self.base_url)
        self.max_depth = max_depth
        self.id_audit = id_audit
        self.id_domaine = id_domaine  # Ajouter l'ID du domaine principal
        self.sous_domaines = []
        self.technologies = []
        self.relations_utiliser = []  # Pour stocker les relations entre domaines et technologies
        self.visited_urls = set()
        self.discovered_urls = set()
        self.url_to_sd_id = {}  # Dictionnaire pour mapper les URLs aux IDs de sous-domaines

    def is_internal_link(self, url):
        """Vérifie si l'URL est interne au domaine."""
        try:
            return urlparse(url).netloc == urlparse(self.base_url).netloc
        except Exception:
            return False

    def normalize_url(self, url):
        """Normalise l'URL pour éviter les doublons, en conservant les paramètres de requête significatifs."""
        try:
            parsed = urlparse(unquote(url))
            # Conserver les paramètres de requête
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized += f"?{parsed.query}"
            return normalized.rstrip('/')
        except Exception:
            return url.rstrip('/')

    def should_crawl_url(self, url, consider_query=True):
        """Détermine si l'URL doit être crawlée."""
        unwanted_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.css', '.js', '.xml', '.json']

        base_checks = (
                self.is_internal_link(url) and
                not any(url.lower().endswith(ext) for ext in unwanted_extensions) and
                url not in self.visited_urls and
                url not in self.discovered_urls
        )

        # Si on considère les paramètres de requête
        if consider_query:
            base_url_without_query = url.split('?')[0]
            return base_checks and not any(
                visited.split('?')[0] == base_url_without_query for visited in self.visited_urls)

        return base_checks

    def extract_links(self, soup, current_url):
        """Extrait tous les liens internes de la page."""
        links = set()
        for link in soup.find_all(['a', 'link'], href=True):
            try:
                href = link.get('href')

                # Construction intelligente de l'URL complète
                if href.startswith('/'):
                    # Si l'URL commence par /, utiliser l'URL de base du domaine
                    full_url = f"{self.base_url}{href}"
                else:
                    # Sinon utiliser urljoin standard
                    full_url = urljoin(current_url, href)

                normalized_url = self.normalize_url(full_url)

                if self.should_crawl_url(normalized_url):
                    links.add(normalized_url)
                    self.discovered_urls.add(normalized_url)
            except Exception as e:
                print(f"Error extracting link: {e}")
        return links

    def extract_technologies(self, soup, response=None):
        """Détecte les technologies utilisées sans doublons."""
        tech_patterns = {
            # Frameworks et langages web
            'PHP': ['php', 'index.php', 'x-powered-by: php'],
            'ASP.NET': ['asp.net', 'x-aspnet-version', 'x-powered-by: asp.net'],
            'ASP': ['.asp', 'asp classic'],
            'Ruby on Rails': ['rails', 'x-powered-by: phusion passenger'],
            'Django': ['django', 'x-django-version'],
            'Laravel': ['laravel'],
            'Flask': ['flask'],

            # Serveurs web
            'Apache': ['apache', 'server: apache'],
            'Nginx': ['nginx', 'server: nginx'],
            'IIS': ['iis', 'server: microsoft-iis'],
            'LiteSpeed': ['litespeed', 'server: litespeed'],

            # Frontend frameworks
            'jQuery': ['jquery', 'jquery.min.js'],
            'React': ['react.', 'react-dom'],
            'Vue': ['vue.js', 'vue.min.js'],
            'Angular': ['angular.js', 'angular.min.js'],
            'Bootstrap': ['bootstrap.', 'bootstrap.min.css'],
            'Tailwind': ['tailwind', 'tailwindcss'],
        }

        # Ensembles pour stocker les technologies et leurs noms
        detected_techs = set()
        existing_tech_names = {tech.nom_techno for tech in self.technologies}

        # Détection via les balises et attributs HTML
        server_meta_tags = soup.find_all('meta', attrs={'name': ['generator', 'powered-by']})

        # Détection via les scripts et links
        scripts_and_links = soup.find_all(['script', 'link'], src=True)

        # Détection via les headers HTTP si un objet response est fourni
        headers = response.headers if response else {}

        # Vérification des balises meta
        for meta in server_meta_tags:
            content = meta.get('content', '').lower()
            for tech, patterns in tech_patterns.items():
                if any(pattern in content for pattern in patterns):
                    if tech not in existing_tech_names:
                        detected_techs.add(tech)

        # Vérification des scripts et liens
        for script in scripts_and_links:
            src = script.get('src', '').lower()
            for tech, patterns in tech_patterns.items():
                if any(pattern in src for pattern in patterns):
                    if tech not in existing_tech_names:
                        detected_techs.add(tech)

        # Vérification des headers HTTP
        for tech, patterns in tech_patterns.items():
            for pattern in patterns:
                # Vérifier dans le nom du serveur ou les headers spécifiques
                if any(pattern in str(header).lower() for header in headers.values()):
                    if tech not in existing_tech_names:
                        detected_techs.add(tech)

        # Conversion en modèles de technologie
        techs = []
        for tech in detected_techs:
            version_match = None

            # Tentative d'extraction de version (exemple simplifié)
            for script in scripts_and_links:
                src = script.get('src', '').lower()
                version_match = re.search(r'(\d+\.\d+\.\d+)', src)
                if version_match:
                    break

            tech_model = Technologie(
                nom_techno=tech,
                version_techno=version_match.group(1) if version_match else "1.0.0"  # Version par défaut si non détectée
            )
            techs.append(tech_model)

        return techs

    def crawl_bfs(self):
        """Méthode de crawling utilisant BFS (Breadth-First Search)."""
        # Initialisation avec l'URL de base
        queue = deque([(self.base_url, 0, None)])  # (url, depth, parent_url)
        
        # Ajouter l'URL de base comme premier sous-domaine (domaine racine)
        normalized_base_url = self.normalize_url(self.base_url)
        root_sous_domaine = SousDomaine(
            url_SD=normalized_base_url,
            description_SD="Domaine racine",  # Description par défaut
            degre=0,
            id_domaine=self.id_domaine,  # Lien vers le domaine principal
            id_SD_Sous_domaine=None  # Pas de parent pour la racine
        )
        
        # Ajouter le sous-domaine racine à la liste
        self.sous_domaines.append(root_sous_domaine)
        self.visited_urls.add(normalized_base_url)
        
        # Traiter la file d'attente BFS
        while queue:
            current_url, depth, parent_url = queue.popleft()
            
            # Si la profondeur maximale est atteinte, on passe à l'URL suivante
            if depth > self.max_depth:
                continue
                
            try:
                normalized_url = self.normalize_url(current_url)
                logger.info(f"Crawling: {normalized_url} at depth {depth}")
                
                response = requests.get(normalized_url,
                                        headers={'User-Agent': 'Mozilla/5.0'},
                                        timeout=50)
                
                # Vérifier le type de contenu
                if 'text/html' not in response.headers.get('Content-Type', '').lower():
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Trouver l'ID parent (pour le stockage en BDD)
                parent_id = None
                if parent_url:
                    parent_normalized = self.normalize_url(parent_url)
                    for sd in self.sous_domaines:
                        if sd.url_SD == parent_normalized:
                            parent_id = sd.id_SD
                            break
                
                # Ne pas recréer de sous-domaine pour l'URL racine qui est déjà créée
                sd_id = None
                if normalized_url != normalized_base_url:
                    # Création du SousDomaine
                    sous_domaine = SousDomaine(
                        url_SD=normalized_url,
                        description_SD=f"Sous-domaine de profondeur {depth}",  # Description par défaut
                        degre=depth,
                        id_domaine=self.id_domaine,  # Lien vers le domaine principal
                        id_SD_Sous_domaine=parent_id  # ID du parent
                    )
                    
                    # Ajouter uniquement s'il n'existe pas déjà
                    if not any(sd.url_SD == sous_domaine.url_SD for sd in self.sous_domaines):
                        self.sous_domaines.append(sous_domaine)
                        sd_id = sous_domaine.id_SD  # À utiliser après le flush en BDD
                        self.url_to_sd_id[normalized_url] = len(self.sous_domaines) - 1  # Index dans la liste
                
                # Extraction des technologies
                site_technologies = self.extract_technologies(soup, response)
                for tech in site_technologies:
                    # Ajouter uniquement les technologies qui n'existent pas déjà
                    if not any(t.nom_techno == tech.nom_techno for t in self.technologies):
                        self.technologies.append(tech)
                        
                        # Créer la relation Utiliser entre le domaine et la technologie
                        utiliser = Utiliser(
                            id_domaine=self.id_domaine,
                            id_techno=None  # Sera mis à jour après l'ajout en BDD
                        )
                        self.relations_utiliser.append((utiliser, len(self.technologies) - 1))
                
                # Extraire les liens pour le niveau suivant
                links = self.extract_links(soup, normalized_url)
                
                # Ajouter les nouveaux liens à la file d'attente pour le prochain niveau
                for link in links:
                    if link not in self.visited_urls:
                        queue.append((link, depth + 1, normalized_url))
                        self.visited_urls.add(link)  # Marquer comme visité immédiatement pour éviter les doublons dans la file
                
            except requests.RequestException as e:
                logger.error(f"Erreur de crawl pour {current_url}: {e}")
            except Exception as e:
                logger.error(f"Erreur inattendue lors du crawl de {current_url}: {e}")

    def get_report(self):
        """Génère un rapport du crawling."""
        return {
            "domaine": self.domaine_model,
            "sous_domaines": self.sous_domaines,
            "technologies": self.technologies,
            "relations_utiliser": self.relations_utiliser
        }


def main():
    """Fonction principale pour l'interaction utilisateur."""
    try:
        base_url = input("Entrez l'URL du site à crawler (ex: https://example.com): ").strip()

        # Validation de base de l'URL
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url

        # Demander la profondeur de crawl
        max_depth = int(input("Entrez la profondeur maximale de crawl (par défaut 3): ") or 3)

        # Créer et exécuter le crawler (avec un ID fictif pour tester)
        crawler = WebCrawler(base_url, max_depth=max_depth, id_domaine=1)
        crawler.crawl_bfs()  # Utiliser BFS au lieu de la méthode récursive

        # Générer et afficher le rapport
        rapport = crawler.get_report()

        print("\n--- Rapport de Crawling ---")
        print("\nDomaine:", rapport["domaine"])

        print("\n--- Technologies Détectées ---")
        for tech in rapport["technologies"]:
            print(tech)

        print("\n--- Sous-Domaines ---")
        for sd in sorted(rapport["sous_domaines"], key=lambda x: x.degre):
            print(sd)

        print(f"\nTotal de sous-domaines découverts : {len(rapport['sous_domaines'])}")

    except ValueError:
        print("Profondeur invalide. Utilisez un nombre entier.")
    except requests.RequestException:
        print("Impossible de se connecter à l'URL. Vérifiez l'URL et votre connexion internet.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    main()