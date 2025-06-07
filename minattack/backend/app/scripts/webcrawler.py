import asyncio
import difflib
import aiohttp
from typing import List, Tuple, Set
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import re
from collections import deque
import json
import time
import logging
import csv
import hashlib

from minattack.backend.app.models.domaine import Domaine
from minattack.backend.app.models.sous_domaine import SousDomaine
from minattack.backend.app.models.technologie import Technologie
from minattack.backend.app.models.utiliser import Utiliser
from minattack.backend.app.models.vecteur import Vecteur
from minattack.backend.app.scripts.init_vector_script import InitVector

logger = logging.getLogger(__name__)

class AsyncWebCrawler:
    """
    Crawler web asynchrone pour la cartographie automatisée de sites web.
    Supporte le fuzzing parallèle et la détection de technologies.
    """
    
    def __init__(self, base_url, max_depth=None, max_urls=5000, max_duration_minutes=10, 
                 id_domaine=None, fuzzing=False, wordlist_path=None):
        """
        Initialise le crawler avec configuration asynchrone.
        
        Args:
            base_url: URL racine à analyser
            max_depth: Profondeur maximale de crawling
            max_urls: Limite du nombre d'URLs à traiter
            max_duration_minutes: Durée maximale d'exécution
            id_domaine: Identifiant du domaine en base
            fuzzing: Active le test de chemins par wordlist
            wordlist_path: Chemin vers le fichier de wordlist
        """
        self.base_url = base_url.rstrip('/')
        self.domaine_model = Domaine(url_domaine=self.base_url)
        
        # Configuration de profondeur adaptative
        if max_depth is None:
            self.max_depth = self._estimate_reasonable_depth(base_url)
            logger.info(f"Profondeur estimée automatiquement: {self.max_depth}")
        else:
            self.max_depth = max_depth
            
        # Limites de sécurité
        self.max_urls = max_urls
        self.max_duration = max_duration_minutes * 60
        self.start_time = time.time()

        # Configuration réseau asynchrone
        self.max_concurrent_requests = 20
        self.request_timeout = 6
        
        # Configuration du fuzzing
        self.fuzzing = fuzzing
        self.wordlist_path = None
        self.wordlist_words = []
        
        if fuzzing and wordlist_path:
            self.wordlist_path = wordlist_path
            self.wordlist_words = self._load_wordlist(wordlist_path)[:30]
            logger.info(f"Fuzzing activé avec {len(self.wordlist_words)} mots de test")
        elif fuzzing and not wordlist_path:
            logger.warning("Fuzzing demandé sans wordlist - désactivation automatique")
            self.fuzzing = False
        else:
            logger.info("Mode crawling standard - fuzzing désactivé")
        
        # Codes de statut HTTP intéressants à collecter
        self.interesting_status_codes: Set[int] = {
            # Succès 2xx
            200, 201, 202, 203, 204, 205, 206,
            # Erreurs client 4xx (sauf 404 et redirections)
            400, 401, 402, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 451,
            # Erreurs serveur 5xx
            500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511
        }
        
        # Identifiants de base de données
        self.id_domaine = id_domaine
        
        # Collections de données collectées
        self.sous_domaines = []
        self.technologies = []
        self.vecteurs = []
        self.relations_utiliser = []
        
        # État du processus de crawling
        self.visited_urls = set()
        self.discovered_urls = set()
        self.url_to_sd_id = {}
        self.url_to_content = {}
        self.parent_child_map = {}
        
        # Cache de performance pour optimiser les opérations répétitives
        self._url_base_cache = {}
        
        # Métriques et statistiques de performance
        self.stats = {
            'urls_processed': 0,
            'urls_skipped_depth': 0,
            'urls_skipped_limit': 0,
            'urls_skipped_time': 0,
            'urls_skipped_type': 0,
            'urls_from_wordlist': 0,
            'errors': 0,
            'async_requests': 0,
            'status_codes_found': {},
            'fuzzing_time': 0
        }
        # Mémoire des dernières URLs valides pour éviter les "fausses 200" (soft 404)
        self.recent_valid_urls = deque(maxlen=15)  # nombre de dernières URLs à mémoriser
        self.similarity_threshold = 0.92  # seuil de similarité entre 0 et 1
        self.similarity_count_threshold = 5 
    
    def is_similar_to_recent(self, url: str) -> bool:
        """
        Vérifie si l'URL est trop similaire à plusieurs récemment acceptées.
        Utilisé pour détecter les faux positifs HTTP 200 (soft 404).
        """
        count_similar = 0
        for recent_url in self.recent_valid_urls:
            similarity = difflib.SequenceMatcher(None, recent_url, url).ratio()
            if similarity >= self.similarity_threshold:
                count_similar += 1
        return count_similar >= self.similarity_count_threshold

    def _estimate_reasonable_depth(self, base_url: str) -> int:
        """
        Estime une profondeur de crawling appropriée selon le type de site.
        
        Returns:
            int: Profondeur recommandée
        """
        url_lower = base_url.lower()
        
        # Sites de test et démonstration - profondeur réduite
        test_keywords = ['test', 'demo', 'vulnweb', 'dvwa', 'webgoat', 'mutillidae', 'bwapp']
        if any(keyword in url_lower for keyword in test_keywords):
            logger.info("Site de test détecté - profondeur réduite appliquée")
            return 3
            
        # Sites avec architectures profondes connues
        deep_keywords = ['blog', 'wiki', 'forum', 'shop', 'store', 'news']
        if any(keyword in url_lower for keyword in deep_keywords):
            logger.info("Architecture profonde détectée - profondeur étendue appliquée")
            return 6
            
        return 5

    def _load_wordlist(self, wordlist_path: str) -> List[str]:
        """
        Charge et filtre une wordlist depuis un fichier CSV.
        
        Args:
            wordlist_path: Chemin vers le fichier wordlist
            
        Returns:
            List[str]: Liste des mots valides pour le fuzzing
        """
        words = []
        try:
            with open(wordlist_path, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and len(row) > 0:
                        word = row[0].strip()
                        # Filtrage des entrées valides
                        if word and not word.startswith('#') and 2 <= len(word) <= 20:
                            words.append(word)
            logger.info(f"Wordlist chargée: {len(words)} entrées valides depuis {wordlist_path}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la wordlist {wordlist_path}: {e}")
        return words

    def normalize_url(self, url):
        """
        Normalise les URLs pour éviter les doublons avec mise en cache.
        
        Args:
            url: URL à normaliser
            
        Returns:
            str: URL normalisée
        """
        if url in self._url_base_cache:
            return self._url_base_cache[url]
            
        try:
            parsed = urlparse(unquote(url))
            normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized += f"?{parsed.query}"
            result = normalized.rstrip('/')
            self._url_base_cache[url] = result
            return result
        except Exception:
            return url.rstrip('/')

    def is_internal_link(self, url):
        """
        Vérifie si une URL appartient au domaine cible.
        
        Args:
            url: URL à vérifier
            
        Returns:
            bool: True si l'URL est interne au domaine
        """
        try:
            return urlparse(url).netloc == urlparse(self.base_url).netloc
        except Exception:
            return False

    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> Tuple[str, int, str, dict]:
        """
        Effectue une requête HTTP asynchrone sur une URL.
        
        Args:
            session: Session aiohttp réutilisable
            url: URL cible
            
        Returns:
            Tuple[str, int, str, dict]: URL, code statut, contenu, headers
        """
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=self.request_timeout),
                allow_redirects=False,
                ssl=False
            ) as response:
                self.stats['async_requests'] += 1
                status_code = response.status
                
                # Comptabilisation des codes de statut
                self.stats['status_codes_found'][status_code] = \
                    self.stats['status_codes_found'].get(status_code, 0) + 1
                
                # Lecture conditionnelle du contenu
                content = ""
                if status_code in self.interesting_status_codes:
                    content_type = response.headers.get('Content-Type', '').lower()
                    if 'text/html' in content_type:
                        content = await response.text(errors='ignore')
                    
                return url, status_code, content, dict(response.headers)
                
        except asyncio.TimeoutError:
            logger.debug(f"Timeout lors de la requête: {url}")
            return url, 0, "", {}
        except aiohttp.ClientError as e:
            logger.debug(f"Erreur client pour {url}: {e}")
            return url, 0, "", {}
        except Exception as e:
            logger.debug(f"Erreur inattendue pour {url}: {e}")
            self.stats['errors'] += 1
            return url, 0, "", {}

    async def test_wordlist_paths_async(self, base_url: str) -> List[Tuple[str, int, str]]:
        """
        Exécute le fuzzing asynchrone avec détection avancée des pièges à fuzzing.
        Utilise des techniques multi-niveaux pour éviter les faux positifs.
        """
        if not self.fuzzing or not self.wordlist_words:
            return []

        base_url = base_url.rstrip('/')
        fuzzing_start = time.time()

        test_urls = []
        for word in self.wordlist_words:
            word = word.strip().strip('/')
            if not word:
                continue

            word_urls = [
                f"{base_url}/{word}",
                f"{base_url}/{word}.php",
                f"{base_url}/{word}.html",
                f"{base_url}/{word}.asp",
                f"{base_url}/{word}.aspx",
                f"{base_url}/{word}.jsp",
                f"{base_url}/{word}.txt",
            ]
            if '.' not in word:
                word_urls.append(f"{base_url}/{word}/")

            for test_url in word_urls:
                normalized_url = self.normalize_url(test_url)
                if (normalized_url not in self.visited_urls and 
                    self.is_internal_link(normalized_url)):
                    test_urls.append(normalized_url)

        if not test_urls:
            return []

        logger.info(f"🔍 Fuzzing anti-piège: test de {len(test_urls)} URLs")

        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent_requests,
            limit_per_host=self.max_concurrent_requests,
            ttl_dns_cache=300,
            use_dns_cache=True,
            enable_cleanup_closed=True
        )
        timeout = aiohttp.ClientTimeout(total=self.request_timeout)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        discovered_urls = []
        
        # 🔬 SYSTÈME DE DÉTECTION MULTI-NIVEAUX
        response_patterns = {}          # Patterns de réponse identiques
        content_hashes = {}            # Hash complets du contenu
        content_structures = {}        # Structure DOM simplifiée
        response_times = []            # Temps de réponse pour détection de patterns
        title_patterns = {}           # Titres de pages identiques
        error_baselines = {}          # Baselines d'erreur par code de statut
        dynamic_content_markers = set() # Marqueurs de contenu dynamique
        
        # Variables de seuils adaptatifs
        similarity_threshold = 0.85    # Seuil de similarité de contenu
        structure_threshold = 0.90     # Seuil de similarité structurelle
        duplicate_limit = 3            # Nombre max de contenus identiques
        response_time_variance = 0.15  # Variance acceptable des temps de réponse

        def extract_content_structure(html_content):
            """Extrait la structure DOM simplifiée pour détecter les templates"""
            if not html_content:
                return ""
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Suppression du contenu variable
                for tag in soup.find_all(['title', 'meta']):
                    tag.decompose()
                for tag in soup.find_all(string=True):
                    if tag.strip():
                        tag.replace_with('[TEXT]')
            
                # Extraction de la structure des balises
                structure = []
                for tag in soup.find_all():
                    tag_info = f"{tag.name}"
                    if tag.get('class'):
                        tag_info += f".{'.'.join(tag['class'])}"
                    if tag.get('id'):
                        tag_info += f"#{tag['id']}"
                    structure.append(tag_info)
            
                return '|'.join(structure[:50])  # Limite pour performance
            except:
                return ""

        def extract_page_title(html_content):
            """Extrait le titre de la page"""
            if not html_content:
                return ""
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                title_tag = soup.find('title')
                return title_tag.get_text().strip() if title_tag else ""
            except:
                return ""

        def calculate_content_entropy(content):
            """Calcule l'entropie du contenu pour détecter les pages génériques"""
            if not content:
                return 0
            import math
            from collections import Counter
            
            # Analyse par caractères
            char_freq = Counter(content.lower())
            total_chars = len(content)
            
            entropy = 0
            for count in char_freq.values():
                probability = count / total_chars
                if probability > 0:
                    entropy -= probability * math.log2(probability)
            
            return entropy

        def detect_dynamic_markers(content):
            """Détecte les marqueurs de contenu dynamique (timestamps, sessions, etc.)"""
            import re
            dynamic_patterns = [
                r'\b\d{4}-\d{2}-\d{2}\b',           # Dates YYYY-MM-DD
                r'\b\d{2}:\d{2}:\d{2}\b',           # Heures HH:MM:SS
                r'\bsession[_\-]?id["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]+', # Session IDs
                r'\btimestamp["\']?\s*[:=]\s*["\']?\d+',  # Timestamps
                r'\bnonce["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]+', # Nonces
                r'\bcsrf[_\-]?token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]+', # CSRF tokens
                r'\b[a-f0-9]{32,}\b',                # Hash MD5/SHA
                r'\buuid["\']?\s*[:=]\s*["\']?[a-f0-9-]{36}', # UUIDs
            ]
            
            markers = set()
            for pattern in dynamic_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                markers.update(matches)
            
            return markers

        def is_recursive_path(url):
            """Détecte les chemins récursifs"""
            path = urlparse(url).path
            segments = path.strip("/").split("/")
            return len(segments) != len(set(segments))

        def advanced_content_analysis(url, status_code, content, response_time):
            """
            Analyse avancée multi-critères pour détecter les pièges
            Retourne True si l'URL semble être un piège
            """
            if not content:
                return status_code != 403  # Les 403 sans contenu sont souvent valides
            
            # ANALYSE DE L'ENTROPIE
            entropy = calculate_content_entropy(content)
            if entropy < 3.5:  # Entropie très faible = contenu répétitif
                logger.debug(f"Entropie faible détectée: {url} (entropie: {entropy:.2f})")
                return True
            
            # ANALYSE DU TITRE DE PAGE
            page_title = extract_page_title(content)
            if page_title:
                title_key = page_title.lower().strip()
                if title_key in title_patterns:
                    title_patterns[title_key].append(url)
                    if len(title_patterns[title_key]) > duplicate_limit:
                        logger.debug(f"Titre dupliqué: {url} (titre: '{page_title[:50]}...')")
                        return True
                else:
                    title_patterns[title_key] = [url]
            
            # ANALYSE DE LA STRUCTURE DOM
            content_structure = extract_content_structure(content)
            if content_structure:
                if content_structure in content_structures:
                    content_structures[content_structure].append(url)
                    if len(content_structures[content_structure]) > duplicate_limit:
                        logger.debug(f"Structure DOM identique: {url}")
                        return True
                else:
                    content_structures[content_structure] = [url]
            
            #HASH COMPLET DU CONTENU
            content_hash = hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest()
            if content_hash in content_hashes:
                content_hashes[content_hash].append(url)
                if len(content_hashes[content_hash]) > 2:  # Limite stricte pour hash complet
                    logger.debug(f"Contenu identique détecté: {url}")
                    return True
            else:
                content_hashes[content_hash] = [url]
            
            # DÉTECTION DE CONTENU DYNAMIQUE SUSPECT
            dynamic_markers = detect_dynamic_markers(content)
            if len(dynamic_markers) > 5:  # Trop de contenu dynamique = suspect
                logger.debug(f"Trop de contenu dynamique: {url} ({len(dynamic_markers)} marqueurs)")
                return True
            
            # ANALYSE DES TEMPS DE RÉPONSE
            response_times.append(response_time)
            if len(response_times) > 10:
                avg_time = sum(response_times[-10:]) / 10
                if abs(response_time - avg_time) / avg_time > response_time_variance:
                    # Temps de réponse anormal = potentiel traitement spécial
                    pass  # Pour l'instant on ne rejette pas sur ce critère
            
            #PATTERNS DE RÉPONSE IDENTIQUES (status + taille + début contenu)
            content_preview = content[:200] if content else ""
            response_pattern = (status_code, len(content), hash(content_preview))
            
            if response_pattern in response_patterns:
                response_patterns[response_pattern].append(url)
                if len(response_patterns[response_pattern]) > duplicate_limit + 2:
                    logger.debug(f"🚫 Pattern de réponse identique: {url} (pattern: {response_pattern})")
                    return True
            else:
                response_patterns[response_pattern] = [url]
            
            # DÉTECTION D'ERREURS SPÉCIALISÉES
            content_lower = content.lower()
            
            # Erreurs 200 déguisées
            if status_code == 200:
                soft_404_patterns = [
                    'not found', 'page not found', 'file not found', '404 error',
                    'page does not exist', 'nothing found here', 'no such page',
                    'the requested url was not found', 'sorry, page not found',
                    'oops! page not found', 'error: page not found',
                    'this page doesn\'t exist', 'page unavailable',
                    'requested resource was not found', 'content not available'
                ]
                
                soft_404_score = sum(1 for pattern in soft_404_patterns if pattern in content_lower)
                if soft_404_score >= 2:  # Plusieurs indicateurs = soft 404
                    logger.debug(f"Soft 404 détecté: {url} (score: {soft_404_score})")
                    return True
            
            # ANALYSE BASELINE PAR CODE DE STATUT
            if status_code in error_baselines:
                baseline_content = error_baselines[status_code]
                similarity = difflib.SequenceMatcher(None, content, baseline_content).ratio()
                if similarity > similarity_threshold:
                    logger.debug(f"Réponse baseline identique: {url} (similarité: {similarity:.2f})")
                    return True
            else:
                # Établir une baseline pour ce code de statut
                if len(content) > 100:  # Seulement pour les contenus substantiels
                    error_baselines[status_code] = content
            
            return False  # URL semble valide

        # EXÉCUTION DES REQUÊTES ASYNCHRONES
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        ) as session:
            semaphore = asyncio.Semaphore(self.max_concurrent_requests)

            async def limited_fetch(url):
                async with semaphore:
                    start_time = time.time()
                    result = await self.fetch_url(session, url)
                    response_time = time.time() - start_time
                    return result + (response_time,)

            # Filtrer les URLs récursives avant le test
            valid_test_urls = [url for url in test_urls if not is_recursive_path(url)]
            tasks = [limited_fetch(url) for url in valid_test_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # ANALYSE DES RÉSULTATS
            for result in results:
                if isinstance(result, Exception):
                    self.stats['errors'] += 1
                    continue

                url, status_code, content, headers_dict, response_time = result

                if status_code not in self.interesting_status_codes:
                    continue

                try:
                    # APPLICATION DE L'ANALYSE ANTI-PIÈGE
                    is_trap = advanced_content_analysis(url, status_code, content, response_time)
                    
                    if is_trap:
                        logger.debug(f"PIÈGE DÉTECTÉ: {url} [{status_code}]")
                        continue

                    # URL VALIDÉE - Ajouter aux résultats
                    discovered_urls.append((url, status_code, content))
                    self.stats['urls_from_wordlist'] += 1
                    
                    if content:
                        self.url_to_content[url] = content

                    status_category = (
                        "Success" if 200 <= status_code < 300 else
                        "Redirect" if 300 <= status_code < 400 else
                        "Client Error" if 400 <= status_code < 500 else
                        "Server Error" if 500 <= status_code < 600 else
                        "Unknown"
                    )
                    
                    logger.info(f"URL VALIDE: {url} [{status_code} - {status_category}] ({len(content) if content else 0} bytes)")

                except Exception as e:
                    logger.debug(f"Erreur lors de l'analyse de {url}: {e}")
                    continue
        fuzzing_elapsed = time.time() - fuzzing_start
        self.stats['fuzzing_time'] += fuzzing_elapsed

        logger.info(f"🎯 Fuzzing anti-piège terminé: {len(discovered_urls)} URLs authentiquement valides")
        logger.info(f"Performance: {len(valid_test_urls)/fuzzing_elapsed:.1f} req/s")
        
        # Statistiques de filtrage
        total_tested = len(valid_test_urls)
        total_filtered = total_tested - len(discovered_urls)
        filter_rate = (total_filtered / total_tested) * 100 if total_tested > 0 else 0
        
        logger.info(f"Taux de filtrage des pièges: {filter_rate:.1f}% ({total_filtered}/{total_tested})")
        
        if discovered_urls:
            status_summary = {}
            for _, status, _ in discovered_urls:
                status_summary[status] = status_summary.get(status, 0) + 1
            status_str = ", ".join([f"{status}({count})" for status, count in sorted(status_summary.items())])
            logger.info(f"Distribution des codes valides: {status_str}")

        return discovered_urls

    

    def extract_links(self, soup, current_url):
        """
        Extrait les liens internes depuis le contenu HTML d'une page.
        
        Args:
            soup: Objet BeautifulSoup du contenu HTML
            current_url: URL de la page courante
            
        Returns:
            set: Ensemble des URLs internes découvertes
        """
        links = set()
        
        # Extraction des liens depuis les éléments HTML
        link_elements = soup.find_all(['a', 'area'], href=True)
        form_elements = soup.find_all('form', action=True)
        
        base_parsed = urlparse(self.base_url)
        
        for element in link_elements:
            try:
                href = element.get('href', '').strip()
                
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', 'ftp:')):
                    continue
                    
                # Ignorer les ancres sans paramètres
                if href.startswith('#') and '?' not in href:
                    continue

                # Construction des URLs absolues
                if href.startswith('/'):
                    full_url = f"{base_parsed.scheme}://{base_parsed.netloc}{href}"
                elif href.startswith('http'):
                    full_url = href
                else:
                    full_url = urljoin(current_url, href)

                normalized_url = self.normalize_url(full_url)
                
                if (self.is_internal_link(normalized_url) and 
                    normalized_url not in self.visited_urls and 
                    normalized_url not in self.discovered_urls):
                    links.add(normalized_url)
                    self.discovered_urls.add(normalized_url)
                    
            except Exception as e:
                logger.debug(f"Erreur lors de l'extraction du lien {href}: {e}")
    
        # Extraction des actions de formulaires
        for form in form_elements:
            try:
                action = form.get('action', '').strip()
                if action and not action.startswith(('javascript:', 'mailto:', 'ftp:')):
                    if action.startswith('/'):
                        full_url = f"{base_parsed.scheme}://{base_parsed.netloc}{action}"
                    else:
                        full_url = urljoin(current_url, action)
                        
                    normalized_url = self.normalize_url(full_url)
                    if (self.is_internal_link(normalized_url) and 
                        normalized_url not in self.visited_urls):
                        links.add(normalized_url)
                        
            except Exception as e:
                logger.debug(f"Erreur lors de l'extraction du formulaire: {e}")
    
        logger.info(f"Extraction de liens depuis {current_url}: {len(links)} liens découverts")
        return links

    def extract_technologies(self, soup, headers=None):
        """
        Détecte les technologies web utilisées par le site.
        
        Args:
            soup: Contenu HTML parsé
            headers: Headers HTTP de la réponse
            
        Returns:
            List[Technologie]: Liste des technologies détectées
        """
        tech_patterns = {
            'PHP': ['php', 'x-powered-by: php', '<?php'],
            'Nginx': ['nginx', 'server: nginx'],
            'Apache': ['apache', 'server: apache'],
            'IIS': ['iis', 'server: microsoft-iis', 'x-powered-by: asp.net'],
            'jQuery': ['jquery', 'jquery.min.js', 'jquery-'],
            'Bootstrap': ['bootstrap', 'bootstrap.min.css', 'bootstrap-'],
            'WordPress': ['wp-content', 'wp-includes', 'wp-admin'],
            'Drupal': ['drupal', 'sites/default/files'],
            'Joomla': ['joomla', 'media/jui'],
            'React': ['react.js', 'react.min.js', '_react'],
            'Vue.js': ['vue.js', 'vue.min.js'],
            'Angular': ['angular.js', 'angular.min.js'],
            'ASP.NET': ['asp.net', 'x-aspnet-version', 'webforms'],
            'Django': ['django', 'x-django-version'],
            'Laravel': ['laravel', 'laravel_session'],
            'Express': ['express', 'x-powered-by: express'],
            'Node.js': ['node.js', 'x-powered-by: node']
        }

        detected_techs = set()
        existing_tech_names = {tech.nom_techno for tech in self.technologies}

        # Détection via les headers HTTP
        if headers:
            for tech, patterns in tech_patterns.items():
                if tech not in existing_tech_names and tech not in detected_techs:
                    for pattern in patterns:
                        if any(pattern.lower() in str(header).lower() for header in headers.values()):
                            detected_techs.add(tech)
                            break

        # Détection via les ressources JavaScript et CSS
        scripts_and_links = soup.find_all(['script', 'link'], src=True)
        for script in scripts_and_links:
            src = script.get('src', '').lower()
            for tech, patterns in tech_patterns.items():
                if tech not in existing_tech_names and tech not in detected_techs:
                    if any(pattern.lower() in src for pattern in patterns):
                        detected_techs.add(tech)

        # Conversion en objets modèle
        techs = []
        for tech in detected_techs:
            tech_model = Technologie(nom_techno=tech, version_techno="1.0.0")
            techs.append(tech_model)

        return techs

    def generate_vector_for_url(self, url, html_content):
        """
        Génère un vecteur de caractéristiques pour une URL donnée.
        
        Args:
            url: URL analysée
            html_content: Contenu HTML de la page
            
        Returns:
            Tuple[Vecteur, dict]: Vecteur généré et caractéristiques actives
        """
        try:
            if not html_content or len(html_content.strip()) < 10:
                return None, {}
                
            vector_generator = InitVector(html_content)
            vector_array = vector_generator.get_vector()
            vector_json = json.dumps(vector_array.tolist())
            
            vecteur = Vecteur(
                vecteur=vector_json,
                cluster=None,
                id_SD=None
            )
            
            return vecteur, vector_generator.get_active_features()
            
        except Exception as e:
            logger.debug(f"Erreur lors de la génération du vecteur pour {url}: {e}")
            return None, {}

    async def crawl_bfs_async(self):
        """
        Processus principal de crawling utilisant un parcours en largeur asynchrone.
        """
        logger.info(f"Démarrage du crawling asynchrone pour {self.base_url}")
        logger.info(f"Configuration: profondeur={self.max_depth}, URLs_max={self.max_urls}")
        logger.info(f"Mode fuzzing: {'ACTIVÉ' if self.fuzzing else 'DÉSACTIVÉ'}")
        
        import requests
        
        queue = deque([(self.base_url, 0, None)])
        
        normalized_base_url = self.normalize_url(self.base_url)
        root_sous_domaine = SousDomaine(
            url_SD=normalized_base_url,
            description_SD="Domaine racine",
            degre=0,
            id_domaine=self.id_domaine,
            id_SD_Sous_domaine=None
        )
        
        self.sous_domaines.append(root_sous_domaine)
        self.url_to_sd_id[normalized_base_url] = 0
        
        while queue:
            current_url, depth, parent_url = queue.popleft()
            
            normalized_url = self.normalize_url(current_url)
            
            if normalized_url in self.visited_urls:
                continue
            
            # Vérification des contraintes de sécurité
            if not self.should_crawl_url(normalized_url, depth):
                continue
                
            try:
                logger.info(f"Crawling: {normalized_url} (profondeur {depth}/{self.max_depth})")
                
                self.visited_urls.add(normalized_url)
                
                # Requête HTTP synchrone pour le crawling principal
                response = requests.get(
                    normalized_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                    timeout=10,
                    allow_redirects=False
                )
                
                if 'text/html' not in response.headers.get('Content-Type', '').lower():
                    self.stats['urls_skipped_type'] += 1
                    continue
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                self.url_to_content[normalized_url] = response.text
                self.stats['urls_processed'] += 1
                
                # Établissement des relations hiérarchiques
                if parent_url:
                    normalized_parent = self.normalize_url(parent_url)
                    self.parent_child_map[normalized_url] = normalized_parent
                    logger.debug(f"Relation parent-enfant: {normalized_url} -> {normalized_parent}")
                
                # Création de l'entité sous-domaine (sauf pour l'URL de base)
                sd_index = None
                if normalized_url != normalized_base_url:
                    sous_domaine = SousDomaine(
                        url_SD=normalized_url,
                        description_SD=f"Sous-domaine de profondeur {depth}",
                        degre=depth,
                        id_domaine=self.id_domaine,
                        id_SD_Sous_domaine=None
                    )
                    
                    if not any(sd.url_SD == sous_domaine.url_SD for sd in self.sous_domaines):
                        self.sous_domaines.append(sous_domaine)
                        sd_index = len(self.sous_domaines) - 1
                        self.url_to_sd_id[normalized_url] = sd_index
                        logger.debug(f"Sous-domaine créé pour {normalized_url} (index: {sd_index})")
                else:
                    sd_index = 0
                
                # Génération du vecteur de caractéristiques
                vecteur, _ = self.generate_vector_for_url(normalized_url, response.text)
                if vecteur:
                    vecteur.id_SD = sd_index
                    self.vecteurs.append(vecteur)
                    logger.debug(f"Vecteur créé pour {normalized_url}")
                
                # Détection et catalogage des technologies
                site_technologies = self.extract_technologies(soup, dict(response.headers))
                for tech in site_technologies:
                    if not any(t.nom_techno == tech.nom_techno for t in self.technologies):
                        self.technologies.append(tech)
                        utiliser = Utiliser(id_domaine=self.id_domaine, id_techno=None)
                        self.relations_utiliser.append((utiliser, len(self.technologies) - 1))
        
                # Extraction des liens de navigation
                links = self.extract_links(soup, normalized_url)
                logger.info(f"Liens extraits de {normalized_url}: {len(links)} liens")
                
                # ===== Fuzzing asynchrone si activé =====
                if self.fuzzing and self.wordlist_words and depth < self.max_depth:
                    logger.info(f"Démarrage du fuzzing asynchrone pour {normalized_url}")
                    
                    fuzzing_results = await self.test_wordlist_paths_async(normalized_url)
                    
                    # Traitement des résultats du fuzzing
                    for fuzz_url, status_code, content in fuzzing_results:
                        if fuzz_url not in self.visited_urls:
                            # Création d'entité pour chaque URL découverte par fuzzing
                            fuzz_sous_domaine = SousDomaine(
                                url_SD=fuzz_url,
                                description_SD=f"Découvert par fuzzing (HTTP {status_code})",
                                degre=depth + 1,
                                id_domaine=self.id_domaine,
                                id_SD_Sous_domaine=None
                            )
                            
                            self.sous_domaines.append(fuzz_sous_domaine)
                            fuzz_sd_index = len(self.sous_domaines) - 1
                            self.url_to_sd_id[fuzz_url] = fuzz_sd_index
                            
                            # Établissement de la relation parent-enfant
                            self.parent_child_map[fuzz_url] = normalized_url
                            
                            # Génération de vecteur pour l'URL fuzzée
                            if content:
                                fuzz_vecteur, _ = self.generate_vector_for_url(fuzz_url, content)
                                if fuzz_vecteur:
                                    fuzz_vecteur.id_SD = fuzz_sd_index
                                    self.vecteurs.append(fuzz_vecteur)
                        
                            queue.append((fuzz_url, depth + 1, normalized_url))
                            logger.debug(f"Fuzzing: URL ajoutée à la queue: {fuzz_url}")
                            
            
                # Ajout des liens découverts à la queue
                for link in links:
                    if self.should_crawl_url(link, depth + 1):
                        queue.append((link, depth + 1, normalized_url))
                        logger.debug(f"Lien ajouté à la queue: {link}")
                    else:
                        logger.debug(f"Lien rejeté par les critères: {link}")
            
                # Logging périodique de progression
                if len(self.visited_urls) % 10 == 0:
                    elapsed = time.time() - self.start_time
                    logger.info(f"Progression: {len(self.visited_urls)} URLs visitées, "
                            f"queue: {len(queue)}, durée: {elapsed/60:.1f} min")
            
            except Exception as e:
                logger.error(f"Erreur lors du traitement de {current_url}: {e}")
                self.stats['errors'] += 1

        # Finalisation et calcul des métriques
        elapsed_total = time.time() - self.start_time
        logger.info(f"Crawling terminé en {elapsed_total/60:.1f} minutes")
        self._log_final_stats()

    def _log_final_stats(self):
        """
        Affiche un rapport détaillé des statistiques de crawling.
        """
        logger.info("=== RAPPORT FINAL DE CRAWLING ASYNCHRONE ===")
        logger.info(f"Mode fuzzing: {'ACTIVÉ' if self.fuzzing else 'DÉSACTIVÉ'}")
        logger.info(f"URLs traitées: {self.stats['urls_processed']}")
        logger.info(f"Requêtes asynchrones: {self.stats['async_requests']}")
        logger.info(f"URLs découvertes par fuzzing: {self.stats['urls_from_wordlist']}")
        logger.info(f"Temps de fuzzing total: {self.stats.get('fuzzing_time', 0):.2f}s")
        logger.info(f"Erreurs rencontrées: {self.stats['errors']}")
        logger.info(f"Sous-domaines cartographiés: {len(self.sous_domaines)}")
        logger.info(f"Technologies détectées: {len(self.technologies)}")
        logger.info(f"Vecteurs générés: {len(self.vecteurs)}")
        
        # Rapport détaillé des codes de statut HTTP
        if self.stats.get('status_codes_found'):
            logger.info("Distribution des codes de statut HTTP:")
            for status, count in sorted(self.stats['status_codes_found'].items()):
                status_description = self._get_status_description(status)
                logger.info(f"  {status} ({status_description}): {count} occurrences")

    def _get_status_description(self, status_code):
        """
        Retourne une description textuelle du code de statut HTTP.
        
        Args:
            status_code: Code de statut HTTP
            
        Returns:
            str: Description du statut
        """
        status_descriptions = {
            200: "OK", 201: "Created", 202: "Accepted", 204: "No Content",
            400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 
            405: "Method Not Allowed", 406: "Not Acceptable", 408: "Request Timeout",
            409: "Conflict", 410: "Gone", 429: "Too Many Requests",
            500: "Internal Server Error", 501: "Not Implemented", 
            502: "Bad Gateway", 503: "Service Unavailable", 504: "Gateway Timeout"
        }
        return status_descriptions.get(status_code, f"HTTP {status_code}")

    def get_parent_url(self, url):
        return self.parent_child_map.get(url, None)

    def _check_safety_limits(self, depth):
        """
        Vérifie si les limites de sécurité du crawling sont respectées.
        
        Args:
            depth: Profondeur actuelle
            
        Returns:
            Tuple[bool, str]: (Peut continuer, raison d'arrêt)
        """
        # Vérification de la profondeur maximale
        if depth > self.max_depth:
            self.stats['urls_skipped_depth'] += 1
            return False, f"profondeur maximale atteinte ({depth} > {self.max_depth})"
        
        # Vérification du nombre d'URLs
        if len(self.visited_urls) >= self.max_urls:
            self.stats['urls_skipped_limit'] += 1
            return False, f"limite d'URLs atteinte ({len(self.visited_urls)} >= {self.max_urls})"
        
        # Vérification de la durée d'exécution
        elapsed = time.time() - self.start_time
        if elapsed > self.max_duration:
            self.stats['urls_skipped_time'] += 1
            return False, f"durée maximale atteinte ({elapsed/60:.1f} min > {self.max_duration/60:.1f} min)"
        
        return True, "OK"

    def should_crawl_url(self, url, current_depth, consider_query=True):
        """
        Détermine si une URL doit être incluse dans le processus de crawling.
        Inclut des vérifications avancées pour éviter les URLs non pertinentes.
        
        Args:
            url: URL à évaluer
            current_depth: Profondeur actuelle
            consider_query: Prendre en compte les paramètres de requête
            
        Returns:
            bool: True si l'URL doit être crawlée
        """
        import re

        # Vérification des limites de sécurité
        can_continue, reason = self._check_safety_limits(current_depth)
        if not can_continue:
            return False

        # Éviter le retraitement des URLs déjà visitées
        if url in self.visited_urls:
            return False
        
        # Normalisation et validation de base de l'URL
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                logger.debug(f"URL malformée rejetée: {url}")
                return False
        except Exception:
            logger.debug(f"Erreur de parsing URL: {url}")
            return False
        
        # Vérification de l'appartenance au domaine
        if not self.is_internal_link(url):
            return False
        
        # Filtrage des extensions de fichiers non pertinentes (élargi)
        unwanted_extensions = (
            # Documents
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp',
            # Images
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.ico',
            # Vidéos et audio
            '.mp4', '.mp3', '.avi', '.mov', '.wmv', '.flv', '.swf', '.wav', '.ogg', '.webm',
            # Archives
            '.zip', '.rar', '.tar', '.gz', '.bz2', '.7z', '.deb', '.rpm',
            # Code et styles
            '.css', '.js', '.scss', '.sass', '.less', '.map',
            # Données
            '.xml', '.json', '.csv', '.txt', '.log',
            # Polices
            '.woff', '.woff2', '.ttf', '.eot', '.otf',
            # Exécutables
            '.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'
        )
        
        # Vérification des extensions
        url_path = parsed_url.path.lower()
        if any(url_path.endswith(ext) for ext in unwanted_extensions):
            logger.debug(f"Extension non pertinente détectée: {url}")
            return False

        # Détection des patterns d'URLs suspects ou non pertinents
        url_lower = url.lower()
        path_lower = parsed_url.path.lower()
        
        # Patterns de chemins à éviter
        suspicious_path_patterns = [
            # Fonctionnalités d'authentification
            '/logout', '/disconnect', '/signout', '/sign-out', '/logoff',
            '/login', '/signin', '/sign-in', '/auth', '/oauth',
            # Actions utilisateur
            '/delete', '/remove', '/destroy', '/purge',
            '/edit', '/modify', '/update', '/change',
            '/add', '/create', '/new', '/insert',
            # API et services
            '/api/', '/rest/', '/graphql/', '/webhook/',
            '/service/', '/services/', '/ws/', '/rpc/',
            # Administration
            '/admin/', '/administrator/', '/manage/', '/control/',
            '/dashboard/', '/panel/', '/backend/',
            # Système et configuration
            '/config/', '/configuration/', '/settings/', '/preferences/',
            '/system/', '/debug/', '/test/', '/dev/',
            # Téléchargements et fichiers
            '/download/', '/downloads/', '/files/', '/uploads/',
            '/attachments/', '/documents/', '/media/',
            # Redirections et liens externes
            '/redirect/', '/goto/', '/link/', '/external/', '/outbound/',
            # Calendrier et événements avec dates
            '/calendar/', '/events/', '/schedule/',
            # Flux et feeds
            '/rss/', '/feed/', '/feeds/', '/atom/',
            # Cache et temporaire
            '/cache/', '/tmp/', '/temp/', '/temporary/',
            # Versions et historique
            '/history/', '/versions/', '/revisions/',
            # Print et export
            '/print/', '/export/', '/pdf/', '/excel/'
        ]
        
        # Vérification des patterns suspects dans le chemin
        if any(pattern in path_lower for pattern in suspicious_path_patterns):
            # Exceptions pour certains patterns importants
            important_exceptions = [
                '/search/', '/category/', '/categories/', '/cat/',
                '/product/', '/products/', '/item/', '/items/',
                '/news/', '/blog/', '/article/', '/articles/',
                '/page/', '/pages/', '/content/'
            ]
            if not any(exception in path_lower for exception in important_exceptions):
                logger.debug(f"Pattern de chemin suspect détecté: {url}")
                return False

        # Détection de patterns dans les paramètres de requête
        if parsed_url.query:
            query_lower = parsed_url.query.lower()
            
            # Patterns de paramètres suspects
            suspicious_query_patterns = [
                # Tokens et sessions
                'token=', 'csrf=', 'nonce=', 'session=', 'sid=',
                'auth=', 'key=', 'api_key=', '_token=',
                # Actions suspectes
                'action=delete', 'action=remove', 'action=logout',
                'do=delete', 'do=remove', 'do=logout',
                # Redirections
                'redirect=', 'return=', 'callback=', 'continue=',
                # Debug et développement
                'debug=', 'test=', 'dev=', 'trace='
            ]
            
            if any(pattern in query_lower for pattern in suspicious_query_patterns):
                logger.debug(f"Paramètre de requête suspect détecté: {url}")
                return False
            
            # Détection de pagination excessive
            import re
            page_patterns = [
                r'page[=:](\d+)', r'p[=:](\d+)', r'offset[=:](\d+)',
                r'start[=:](\d+)', r'from[=:](\d+)'
            ]
            
            for pattern in page_patterns:
                match = re.search(pattern, query_lower)
                if match and int(match.group(1)) > 20:  # Limite pagination
                    logger.debug(f"Pagination excessive détectée: {url}")
                    return False
            
            # Détection de paramètres de session ou tokens longs
            query_params = query_lower.split('&')
            for param in query_params:
                if '=' in param:
                    key, value = param.split('=', 1)
                    # Paramètres avec valeurs très longues (probablement des tokens)
                    if len(value) > 32:
                        logger.debug(f"Token/paramètre long détecté: {url}")
                        return False
                    # Paramètres avec des caractères non alphanumériques (hachage)
                    if len(value) > 16 and not re.match(r'^[a-zA-Z0-9_-]+$', value):
                        logger.debug(f"Paramètre encodé/hash détecté: {url}")
                        return False

        # Détection de profondeur de chemin excessive
        path_segments = [seg for seg in parsed_url.path.split('/') if seg]
        
        # Détection de segments de chemin répétitifs ou suspects
        if len(path_segments) > 3:
            if any(len(segment) > 50 for segment in path_segments):
                logger.debug(f"Segment de chemin trop long détecté: {url}")
                return False
            
            # Segments avec des caractères suspects (IDs encodés, hash)
            suspicious_segment_patterns = [
                r'^[a-f0-9]{32,}$',  # Hash MD5/SHA
                r'^[A-Za-z0-9+/]{20,}={0,2}$',  # Base64
                r'^\d{10,}$',  # Timestamps
                r'^[a-f0-9-]{36}$'  # UUIDs
            ]
            
            for segment in path_segments:
                if any(re.match(pattern, segment) for pattern in suspicious_segment_patterns):
                    logger.debug(f"Segment suspect détecté dans {url}: {segment}")
                    return False

        # Gestion améliorée des doublons avec limitation par URL de base
        if consider_query:
            base_url_without_query = url.split('?')[0].split('#')[0]
            
            # Utilisation du cache pour éviter les recalculs
            cache_key = f"base_count_{base_url_without_query}"
            if cache_key not in self._url_base_cache:
                same_base_count = sum(1 for visited in self.visited_urls 
                                    if visited.split('?')[0].split('#')[0] == base_url_without_query)
                self._url_base_cache[cache_key] = same_base_count
            else:
                same_base_count = self._url_base_cache[cache_key]
            
            max_variants = 2
            if same_base_count >= max_variants:
                logger.debug(f"Limitation appliquée pour {base_url_without_query} - {same_base_count} variantes déjà visitées")
                return False
            
            # Autorisation conditionnelle pour les URLs avec paramètres importants
            if same_base_count > 0 and parsed_url.query:
                important_params = [
                    'id', 'page', 'p', 'cat', 'category', 'categories',
                    'search', 'q', 'query', 'term', 'keyword',
                    'type', 'action', 'view', 'mode',
                    'sort', 'order', 'filter',
                    'tag', 'tags', 'author', 'user'
                ]
                
                query_params = parsed_url.query.lower()
                has_important_param = any(f"{param}=" in query_params for param in important_params)
                
                if not has_important_param:
                    logger.debug(f"URL sans paramètres importants rejetée: {url}")
                    return False
        
        # Détection de boucles dans les URLs (patterns cycliques)
        if current_depth > 2:
            path_parts = parsed_url.path.strip('/').split('/')
            if len(path_parts) >= 4:
                # Détection de cycles simples (A/B/A/B)
                for i in range(len(path_parts) - 3):
                    if (path_parts[i] == path_parts[i + 2] and 
                        path_parts[i + 1] == path_parts[i + 3]):
                        logger.debug(f"Pattern cyclique détecté dans le chemin: {url}")
                        return False
        
        # Validation finale de la longueur d'URL
        if len(url) > 2048:  
            logger.debug(f"URL trop longue rejetée: {url}")
            return False
        
        if self.is_similar_to_recent(url):
            logger.info(f"[SIMILARITY FILTER] URL ignorée car trop proche d'autres récentes : {url}")
            self.stats['urls_skipped_type'] += 1
            return False
        
        return True

def run_async_crawler(base_url, **kwargs):
    """
    Point d'entrée principal pour l'exécution du crawler asynchrone.
    Gère automatiquement la création et la fermeture de l'event loop.
    
    Args:
        base_url: URL de base à analyser
        **kwargs: Arguments de configuration pour AsyncWebCrawler
        
    Returns:
        AsyncWebCrawler: Instance du crawler avec résultats
    """
    async def _run():
        crawler = AsyncWebCrawler(base_url, **kwargs)
        await crawler.crawl_bfs_async()
        return crawler
    
    # Gestion intelligente de l'event loop asyncio
    loop = None
    try:
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(_run_in_new_loop, base_url, kwargs)
                return future.result()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        crawler = loop.run_until_complete(_run())
        return crawler
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du crawler asynchrone: {e}")
        raise
    finally:
        if loop and not loop.is_running():
            try:
                loop.close()
            except:
                pass


def _run_in_new_loop(base_url, kwargs):
    """
    Fonction utilitaire pour exécuter le crawler dans un nouveau thread.
    Utilisée quand un event loop existe déjà dans le thread principal.
    
    Args:
        base_url: URL de base
        kwargs: Arguments de configuration
        
    Returns:
        AsyncWebCrawler: Instance du crawler avec résultats
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        async def _run():
            crawler = AsyncWebCrawler(base_url, **kwargs)
            await crawler.crawl_bfs_async()
            return crawler
        return loop.run_until_complete(_run())
    finally:
        loop.close()