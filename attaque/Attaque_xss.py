from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlencode, parse_qs

class Attaque_xss:
    def __init__(self):
        self.payloads = ["<script>alert('1')</script>", "<img src='x' onerror='alert(1)'>"]
        self.resultats = []

    def run_xss(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                parsed_url = urlparse(url)
                params = parse_qs(parsed_url.query)
                param_names = list(params.keys())

                # Tester les paramètres existants
                self.test_ref_xss(url, param_names)

                # Analyser la page pour découvrir des paramètres potentiels
                discovered_params = self.discover_params_from_html(response.text)
                self.test_ref_xss(url, discovered_params)
        except requests.exceptions.RequestException as e:
            print(f"[ERREUR] Problème avec l'URL {url}: {str(e)}")

        return self.resultats

    def test_ref_xss(self, url, params):
        for param in params:
            for payload in self.payloads:
                test_url = self.construct_url_with_payload(url, param, payload)

                try:
                    response = requests.get(test_url, timeout=10)

                    if self.detect_xss(response.text):
                        print(f"[VULNÉRABLE] {url} - Paramètre {param} vulnérable à XSS Reflected avec {payload}")
                        self.resultats.append({
                            "url": url,
                            "param": param,
                            "payload": payload,
                            "response": response.text[:200]  # Récupérer les 200 premiers caractères de la réponse pour l'analyse
                        })
                except requests.exceptions.RequestException as e:
                    print(f"[ERREUR] Test échoué sur {url} avec {payload}: {str(e)}")

    def discover_params_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        form_params = set()

        # Extraire les noms des champs de formulaire
        for input_tag in soup.find_all('input'):
            if input_tag.get('name'):
                form_params.add(input_tag.get('name'))

        return list(form_params)

    def construct_url_with_payload(self, url, param, payload):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params[param] = payload
        new_query = urlencode(query_params, doseq=True)
        return parsed_url._replace(query=new_query).geturl()

    def detect_xss(self, response_text):
        # Rechercher la présence d'une alerte JavaScript dans la réponse
        if "<script>alert('1')</script>" in response_text or "<img src='x' onerror='alert(1)'>" in response_text:
            return True
        return False
