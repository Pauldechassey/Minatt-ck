import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from app.models.attaque import Attaque
from app.models.faille import Faille
from datetime import datetime

class HeadersCookiesScanner:
    def __init__(self):
        self.resultats = {
            'attaques': [],
            'faille': []
        }
        self.session = requests.Session()

    def run_headers_cookies(self, url, timeout=10):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERREUR] Problème avec l'URL {url}: {e}")
            return None
        
        self._analyze_headers(response, url)
        self._analyze_cookies(response, url)
        
        return self.resultats
    
    def _analyze_headers(self, response, url):
        headers = response.headers
        security_headers = {
            'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
            'X-Content-Type-Options': ['nosniff'],
            'Content-Security-Policy': None,
            'X-XSS-Protection': ['1', '1; mode=block'],
            'Strict-Transport-Security': None,
            'Referrer-Policy': None
        }
        
        for header, valid_values in security_headers.items():
            attaque = Attaque(payload=f"Test {header}", date_attaque=datetime.now(), resultat=0, id_Type=4)
            if header not in headers:
                self._log_vulnerability(url, f"Header: {header}", f"Missing security header: {header}")
                attaque.resultat = 1
            elif valid_values is not None:
                header_value = headers[header].lower()
                if not any(valid.lower() in header_value for valid in valid_values):
                    self._log_vulnerability(url, f"Header: {header}", f"Misconfigured security header: {header}={headers[header]}")
                    attaque.resultat = 1
            self.resultats['attaques'].append(attaque)
        
    def _analyze_cookies(self, response, url):
        cookie_header = response.headers.get("Set-Cookie")
        if not cookie_header:
            return
        
        cookies = SimpleCookie()
        try:
            for header in response.headers.getlist('Set-Cookie'):
                cookies.load(header)
        except Exception:
            pass
        
        for cookie_name, cookie in cookies.items():
            samesite, is_secure, is_httponly = None, 'secure' in str(cookie).lower(), 'httponly' in str(cookie).lower()
            for attr in str(cookie).split(';'):
                if attr.strip().lower().startswith('samesite='):
                    samesite = attr.strip().split('=')[1].lower()
            
            vulnerabilities = []
            if samesite not in ["strict", "lax"]:
                vulnerabilities.append("SameSite missing or weak")
            if not is_secure:
                vulnerabilities.append("non-secure")
            if not is_httponly:
                vulnerabilities.append("non-httponly")
            
            attaque = Attaque(payload=f"Test cookie {cookie_name}", date_attaque=datetime.now(), resultat=0, id_Type=4)
            if vulnerabilities:
                self._log_vulnerability(url, f"Cookie: {cookie_name}", f"Cookie issues: {', '.join(vulnerabilities)}")
                attaque.resultat = 1
            self.resultats['attaques'].append(attaque)
    
    def _log_vulnerability(self, url, element, proof):
        print(f"[VULNÉRABLE] {url} - {element}: {proof}")
        faille = Faille(gravite=6, description=proof, balise=element)
        self.resultats['faille'].append(faille)