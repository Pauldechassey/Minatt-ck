from bs4 import BeautifulSoup
import requests
import base64
import time
import re
import hashlib
import random
from urllib.parse import urlparse, urlencode, parse_qs
from backend.app.models.attaque import Attaque
from backend.app.models.faille import Faille
from datetime import datetime

class XSSScanner:
    def __init__(self):
        self.resultats = {
            'attaques':[],
            'failles' : [],
        }

        self.payloads = [
            "<script>alert(1)</script>",
            "<img src='x' onerror='alert(1)'>",
            '" onmouseover=alert(1)"',
            
        ]
        self.encoded_payloads = [base64.b64encode(p.encode()).decode() for p in self.payloads]
        self.session = requests.Session()
        
        # Ajouter un User-Agent pour éviter d'être bloqué
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr,en-US;q=0.7,en;q=0.3"
        }
        
    def run_xss(self, url):
        """
        Point d'entrée principal pour tester une URL contre les XSS.
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"[AVERTISSEMENT] L'URL {url} a retourné le code {response.status_code}")
                return
            
            # Découvrir les paramètres dans l'URL et le HTML
            parsed_url = urlparse(url)
            params = list(parse_qs(parsed_url.query).keys())
            discovered_params = self.discover_params_from_html(response.text)
            all_params = list(set(params + discovered_params))
                        
            # Tester XSS réfléchi et arrêter en cas de faille
            self.test_reflected_xss(url, all_params)
            self.test_stored_xss(url, discovered_params)

            return self.resultats
                
        except requests.RequestException as e:
            print(f"[ERREUR] Problème avec l'URL {url}: {e}")
        except Exception as e:
            print(f"[ERREUR INATTENDUE] {url}: {str(e)}")
        

    def test_reflected_xss(self, url, params):
        """
        Teste les vulnérabilités XSS réfléchies sur tous les paramètres et s'arrête dès qu'une faille est détectée.
        """
        for param in params:
            unique_id = self.generate_unique_id()
            
            for payload_list in [("standard", self.payloads), ("encodé", self.encoded_payloads)]:
                for payload in payload_list:
                    try:
                        marked_payload = payload.replace("1", f"{unique_id}")
                        test_url = self.construct_url_with_payload(url, param, marked_payload)
                        
                        response = self.session.get(test_url, headers=self.headers, timeout=10)
                        
                        id_prov = f"reflected_xss-{url}-{unique_id}"

                        attaque = Attaque(
                            payload=marked_payload,
                            date_attaque=datetime.now(),
                            resultat=0, # par défaut
                            id_Type=2,
                        )
                        attaque.id_provisoire = id_prov

                        IsFaille = None
                        
                        if response.status_code == 200 and self.detect_xss_injection(response.text, unique_id):
                            print(f"[VULNÉRABLE] {url} - Paramètre {param} vulnérable à XSS Reflected avec : {marked_payload}")
                            
                            attaque.resultat = 1
                            IsFaille = Faille(
                                gravite=7,
                                description=f"Paramètre {param} vulnérable à XSS Reflected",
                                balise=param,
                            )
                            IsFaille.id_provisoire = id_prov

                            self.resultats['attaques'].append(attaque)
                            self.resultats['failles'].append(IsFaille)
                            return  
                        
                        self.resultats['attaques'].append(attaque)
                        
                    except requests.RequestException as e:
                        print(f"[ERREUR] Test échoué sur {url} param={param}: {e}")
                        continue
                    except Exception as e:
                        print(f"[ERREUR INATTENDUE] {url} param={param}: {e}")
                        continue
        

    def test_stored_xss(self, url, params=None):
        """
        Teste si une URL est vulnérable aux attaques XSS stockées avec des payloads dynamiques.
        """
        results = []
        test_session_id = self.generate_unique_id()
        
        if not params:
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    params = self.discover_params_from_html(response.text)
                    if not params:
                        print(f"[INFO] Aucun paramètre détecté pour {url}")
                        return results
                else:
                    print(f"[ERREUR] Impossible d'accéder à {url} - Code {response.status_code}")
                    return None
            except requests.RequestException as e:
                print(f"[ERREUR] Impossible d'accéder à {url} - {str(e)}")
                return results
                
        for param in params:
            for i, base_payload in enumerate(self.payloads):
                try:
                    unique_id = f"{test_session_id}{i}"
                    marked_payload = base_payload.replace("alert(1)", f"alert({unique_id})")
                    
                    id_prov = f"stored_xss-{url}-{unique_id}"

                    attaque = Attaque(
                        payload=marked_payload,
                        date_attaque=datetime.now(),
                        resultat=0, # par défaut
                        id_Type=1,
                    )
                    attaque.id_provisoire = id_prov 
                    
                    if self.submit_payload(url, param, marked_payload):
                        displayed_urls = self.check_payload_display_in_pages(url, unique_id)
                        
                        if displayed_urls:
                            for display_url in displayed_urls:
                                print(f"[VULNÉRABLE] {url} - Paramètre {param} vulnérable à XSS Stored avec {marked_payload}")
                                print(f"[DÉTAIL] Payload trouvé dans {display_url}")
                                
                                attaque.resultat = 1
                                IsFaille = Faille(
                                    gravite=8,
                                    description=f"Paramètre {param} vulnérable à XSS Stored",
                                    balise=param,
                                )
                                IsFaille.id_provisoire = id_prov

                                self.resultats['attaques'].append(attaque)
                                self.resultats['failles'].append(IsFaille)
                                return 
                    
                    self.resultats['attaques'].append(attaque)
                    
                except requests.RequestException as e:
                    print(f"[ERREUR] {url} - {param} - {str(e)}")
                    continue
                except Exception as e:
                    print(f"[ERREUR INATTENDUE] {url} - {param} - {str(e)}")
                    continue
        
        

    def discover_params_from_html(self, html_content):
        """
        Découvre tous les paramètres potentiels dans le contenu HTML.
        """
        params = set()
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for input_tag in soup.find_all(['input', 'textarea']):
                name = input_tag.get('name')
                if name and name not in ['csrf_token', '_token', '_csrf']:
                    params.add(name)
            
            for select_tag in soup.find_all('select'):
                name = select_tag.get('name')
                if name:
                    params.add(name)
            
            # Extraire les paramètres des formulaires (action)
            for form in soup.find_all('form', action=True):
                action = form.get('action')
                if '?' in action:
                    query = urlparse(action).query
                    form_params = parse_qs(query).keys()
                    params.update(form_params)
                    
            # Extraire les paramètres potentiels des URLs de l'application
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if '?' in href:
                    try:
                        query = urlparse(href).query
                        url_params = parse_qs(query).keys()
                        params.update(url_params)
                    except:
                        pass
                        
            # Trouver les paramètres dans les scripts (recherche basique)
            for script in soup.find_all('script'):
                if script.string:
                    # Rechercher des motifs comme "param=", "variable:" dans le JavaScript
                    param_matches = re.findall(r'["\']([a-zA-Z0-9_]+)["\'][\s]*[:=]', script.string)
                    params.update(param_matches)
        except Exception as e:
            print(f"[ERREUR] Échec de l'analyse HTML: {str(e)}")
        
        return list(params)
    
    def generate_unique_id(self):
        """
        Génère un identifiant unique pour tracer un payload particulier.
        """
        random_str = str(random.randint(10000, 99999))
        timestamp = str(int(time.time()))
        unique = hashlib.md5((random_str + timestamp).encode()).hexdigest()[:6]
        return unique
    
    def construct_url_with_payload(self, url, param, payload):
        """
        Construit une URL avec le payload dans le paramètre spécifié.
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params[param] = [payload]
        return parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
    
    def submit_payload(self, url, param, payload):
        """
        Soumet le payload via différentes méthodes.
        """
        success = False
        
        # Méthode 1: POST form-data
        try:
            response = self.session.post(
                url, 
                data={param: payload},
                headers=self.headers,
                timeout=10,
                allow_redirects=True
            )
            if response.status_code in [200, 201, 302]:
                success = True
        except requests.RequestException:
            pass
        
        # Méthode 2: GET avec paramètre dans l'URL
        if not success:
            try:
                get_url = self.construct_url_with_payload(url, param, payload)
                response = self.session.get(get_url, headers=self.headers, timeout=10)
                if response.status_code in [200, 201, 302]:
                    success = True
            except requests.RequestException:
                pass
        
        # Méthode 3: POST JSON
        if not success:
            try:
                json_headers = self.headers.copy()
                json_headers["Content-Type"] = "application/json"
                response = self.session.post(
                    url, 
                    json={param: payload}, 
                    headers=json_headers,
                    timeout=10
                )
                if response.status_code in [200, 201, 302]:
                    success = True
            except requests.RequestException:
                pass
        
        return success
    
    def check_payload_display_in_pages(self, base_url, unique_id):
        """
        Vérifie si le payload est affiché sans échappement sur différentes pages,
        en utilisant l'identifiant unique pour garantir que c'est bien cette injection spécifique.
        """
        if not unique_id:
            print("[ERREUR] unique_id doit être fourni pour vérifier l'affichage du payload")
            return []

        parsed_url = urlparse(base_url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Pages courantes où le XSS pourrait être stocké
        common_paths = [
            "", "/", "/index", "/home", "/profile", "/account",
            "/admin", "/dashboard", "/comments", "/posts", "/messages"
        ]

        # Ajouter des chemins basés sur l'URL de base
        path_parts = parsed_url.path.strip("/").split("/")
        for i in range(1, len(path_parts) + 1):
            common_paths.append("/" + "/".join(path_parts[:i]))

        found_urls = []

        # Vérifier l'URL de base en premier
        try:
            response = self.session.get(base_url, headers=self.headers, timeout=10)
            if response.status_code == 200 and self.detect_xss_injection(response.text, unique_id):
                found_urls.append(base_url)
        except requests.RequestException:
            pass

        # Vérifier les pages communes
        for path in common_paths:
            try:
                url = base_domain + path
                if url in found_urls or url == base_url:
                    continue 

                response = self.session.get(url, headers=self.headers, timeout=5)
                if response.status_code == 200 and self.detect_xss_injection(response.text, unique_id):
                    found_urls.append(url)
            except requests.RequestException:
                continue

        return found_urls


    def detect_xss_injection(self, response_text, unique_id):
        """
        Détecte si l'identifiant unique est injecté dans la page sans échappement.
        """
        if not unique_id:
            return False

        # Vérification simple avec le marqueur
        if f"alert('{unique_id}')" in response_text :
            return True

        # Vérifier si le unique_id est affiché en tant que texte brut
        if unique_id in response_text:
            return True

        # Vérifier si le payload est injecté dans un <script>
        script_pattern = re.compile(r'<script\b[^>]*>(.*?)</script>', re.IGNORECASE | re.DOTALL)
        script_tags = script_pattern.findall(response_text)
        for script in script_tags:
            if unique_id in script:
                return True

        # Vérifier si le payload est injecté dans un attribut HTML
        attr_pattern = re.compile(r'(\w+)\s*=\s*(["\'])(.*?)\2', re.IGNORECASE | re.DOTALL)
        for attr_match in attr_pattern.finditer(response_text):
            if unique_id in attr_match.group(3):
                return True

        return False

    def is_escaped(self, response_text, payload):
        """
        Vérifie si le payload est échappé dans la réponse.
        """
        # Vérifier les différentes méthodes d'échappement
        escape_methods = [
            # HTML escaping
            {'<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;', '&': '&amp;'},
            # JavaScript escaping
            {'<': '\\u003c', '>': '\\u003e', '"': '\\u0022', "'": '\\u0027'},
            # URL encoding
            {'<': '%3C', '>': '%3E', '"': '%22', "'": '%27'},
            # Hex escaping
            {'<': '\\x3c', '>': '\\x3e', '"': '\\x22', "'": '\\x27'},
        ]
        
        for method in escape_methods:
            escaped_payload = payload
            for char, replacement in method.items():
                escaped_payload = escaped_payload.replace(char, replacement)
            
            if escaped_payload in response_text and escaped_payload != payload:
                return True
        
        # Vérifier si le payload est présent dans un contexte de données
        data_contexts = [
            re.compile(r'data-\w+=["\'].*' + re.escape(payload) + r'.*["\']'),
            re.compile(r'value=["\'].*' + re.escape(payload) + r'.*["\']')
        ]
        
        for pattern in data_contexts:
            if pattern.search(response_text):
                return True
        
        return False
    
    def get_resultats(self):
        """
        Retourne les résultats des tests.
        """
        return self.resultats
    