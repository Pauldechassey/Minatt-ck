import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
from backend.app.models.attaque import Attaque
from backend.app.models.faille import Faille
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class HeadersCookiesScanner:
    def __init__(self):
        self.resultats = {
            'attaques': [],
            'failles': []
        }
        self.session = requests.Session()
        # Les en-têtes critiques qui devraient être vérifiés strictement
        self.critical_headers = {
            'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
            'X-Content-Type-Options': ['nosniff']
        }
        # Les en-têtes recommandés mais pas critiques pour tous les sites
        self.recommended_headers = {
            'Content-Security-Policy': None,
            'X-XSS-Protection': ['1', '1; mode=block'],
            'Strict-Transport-Security': None,
            'Referrer-Policy': None
        }
        # Les cookies qui doivent être sécurisés
        self.sensitive_cookie_patterns = [
            r'sess(ion)?',
            r'auth',
            r'token',
            r'jwt',
            r'id',
            r'key'
        ]

    def run_headers_cookies(self, url, timeout=10):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"[ERREUR] Problème avec l'URL {url}: {e}")
            return None
        
        self._analyze_headers(response, url)
        self._analyze_cookies(response, url)
        
        return self.resultats
    
    def _analyze_headers(self, response, url):
        headers = response.headers
        is_https = url.lower().startswith('https://')
        
        self._check_security_headers(headers, self.critical_headers, url, 6, is_critical=True)
        
        if is_https:
            self._check_security_headers(headers, self.recommended_headers, url, 4, is_critical=False)
    
    def _check_security_headers(self, headers, header_dict, url, gravite, is_critical):
        for header, valid_values in header_dict.items():
            id_prov = f"header-{url}-{header}"
            attaque = Attaque(payload=f"Test {header}", date_attaque=datetime.now(), resultat=0, id_Type=4)
            attaque.id_provisoire = id_prov
            
            if header not in headers:
                # Critique uniquement pour les en-têtes essentiels
                if is_critical:
                    description = f"Missing critical security header: {header}"
                    self._log_vulnerability(url, f"Header: {header}", description, id_prov, gravite)
                    attaque.resultat = 1
                else:
                    description = f"Missing recommended security header: {header}"
                    self._log_vulnerability(url, f"Header: {header}", description, id_prov, gravite)
                    attaque.resultat = 1
            elif valid_values is not None:
                header_value = headers[header].lower()
                if not any(valid.lower() in header_value for valid in valid_values):
                    description = f"Misconfigured security header: {header}={headers[header]}"
                    self._log_vulnerability(url, f"Header: {header}", description, id_prov, gravite)
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
            # Si getlist n'est pas disponible, essayer avec get
            try:
                cookies.load(response.headers.get('Set-Cookie', ''))
            except Exception as e:
                logger.warning(f"[ERREUR] Impossible de parser les cookies pour {url}: {e}")
                return
        
        is_https = url.lower().startswith('https://')
        
        for cookie_name, cookie in cookies.items():
            # Déterminer si c'est un cookie sensible
            is_sensitive = any(re.search(pattern, cookie_name, re.IGNORECASE) for pattern in self.sensitive_cookie_patterns)
            
            # Obtenir les attributs du cookie
            samesite = None
            is_secure = 'secure' in str(cookie).lower()
            is_httponly = 'httponly' in str(cookie).lower()
            
            for attr in str(cookie).split(';'):
                if attr.strip().lower().startswith('samesite='):
                    samesite = attr.strip().split('=')[1].lower()
            
            vulnerabilities = []
            
            # Vérifier les attributs de sécurité seulement pour les cookies sensibles ou si HTTPS est utilisé
            if is_sensitive:
                if not is_httponly:
                    vulnerabilities.append("non-httponly (sensible à XSS)")
                
                if is_https and not is_secure:
                    vulnerabilities.append("non-secure (sensible à l'interception)")
                
                if samesite not in ["strict", "lax"]:
                    vulnerabilities.append("SameSite manquant ou faible (sensible à CSRF)")
            
            # Pour les cookies non-sensibles, vérifier uniquement certains critères
            elif is_https and not is_secure:
                vulnerabilities.append("non-secure (risque mineur)")
            
            id_prov = f"cookie-{url}-{cookie_name}"
            attaque = Attaque(payload=f"Test cookie {cookie_name}", date_attaque=datetime.now(), resultat=0, id_Type=4)
            attaque.id_provisoire = id_prov
            
            if vulnerabilities:
                # Déterminer la gravité en fonction de la sensibilité du cookie
                gravite = 7 if is_sensitive else 5
                description = f"Cookie {cookie_name}: {', '.join(vulnerabilities)}"
                self._log_vulnerability(url, f"Cookie: {cookie_name}", description, id_prov, gravite)
                attaque.resultat = 1
            
            self.resultats['attaques'].append(attaque)
    
    def _log_vulnerability(self, url, element, proof, id_prov=None, gravite=6):
        logger.warning(f"[VULNÉRABLE] {url} - {element}: {proof}")
        faille = Faille(gravite=gravite, description=proof, balise=element)
        if id_prov:
            faille.id_provisoire = id_prov
        self.resultats['failles'].append(faille)