import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from app.models.attaque import Attaque
from app.models.faille import Faille
from datetime import datetime
from http.cookies import SimpleCookie
import logging

logger = logging.getLogger(__name__)

class CSRFScanner:
    def __init__(self):
        self.resultats = {
            'attaques': [],
            'failles': []
        }
        self.session = requests.Session()
        
        # Liste étendue de mots-clés pour la protection CSRF
        self.csrf_keywords = [
            'csrf', 'xsrf', 'token', 'nonce', '_token', 'authenticity',
            'verify', 'validation', 'security', 'hash', 'anti'
        ]

    def test_csrf(self, url, timeout=10):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"Error accessing {url}: {e}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Vérifier les différentes méthodes de protection CSRF
        has_csrf_token = self._check_page_for_csrf_token(soup)
        has_csrf_header = self._check_response_headers(response)
        has_csrf_cookie = self._check_cookies_for_csrf(response)
        
        # Analyser les formulaires avec un contexte global de protection
        self._analyze_forms(soup, url, has_csrf_token or has_csrf_header or has_csrf_cookie)
        
        return len(self.resultats['failles']) > 0
    
    def _check_page_for_csrf_token(self, soup):
        # Vérifier les méta tags
        meta_csrf = soup.find('meta', attrs={'name': re.compile(r'csrf|xsrf', re.I)})
        if meta_csrf:
            return True
        
        # Vérifier les scripts pour les tokens CSRF
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and re.search(r'(csrf|xsrf|token|security|verify).*', script.string, re.I):
                return True
                
        # Vérifier les input cachés qui pourraient contenir des tokens globaux
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        for hidden in hidden_inputs:
            if hidden.get('name') and any(keyword in hidden.get('name', '').lower() for keyword in self.csrf_keywords):
                if hidden.get('value') and len(hidden.get('value', '')) > 8:  # Token de longueur significative
                    return True
        
        return False
    
    def _check_response_headers(self, response):
        # Certaines applications utilisent des en-têtes personnalisés pour CSRF
        csrf_headers = ['X-CSRF-Token', 'X-XSRF-Token', 'X-Frame-Options']
        for header in csrf_headers:
            if header in response.headers:
                return True
        return False
    
    def _check_cookies_for_csrf(self, response):
        # Vérifier si des cookies pourraient contenir des tokens CSRF
        cookies = SimpleCookie()
        try:
            for header in response.headers.getlist('Set-Cookie'):
                cookies.load(header)
        except:
            try:
                cookies.load(response.headers.get('Set-Cookie', ''))
            except:
                return False
                
        for cookie_name in cookies:
            if any(keyword in cookie_name.lower() for keyword in self.csrf_keywords):
                return True
                
        return False
    
    def _analyze_forms(self, soup, url, has_global_csrf):
        forms = soup.find_all('form')
        
        # Ignorer l'analyse si aucun formulaire n'est trouvé
        if not forms:
            return
            
        for form in forms:
            action = form.get("action", "")
            action_url = urljoin(url, action) if action else url
            method = form.get("method", "GET").upper()
            
            # N'analyser que les formulaires POST avec des champs sensibles
            if method != "POST":
                continue
                
            # Ignorer les formulaires de recherche simples
            if self._is_search_form(form):
                continue
                
            # Vérifier si le formulaire contient des champs sensibles nécessitant une protection CSRF
            if not self._has_sensitive_fields(form):
                continue
                
            # Vérifier la protection CSRF spécifique au formulaire
            has_form_csrf = self._check_form_for_csrf(form)
            
            id_provisoire = f"csrf-{action_url}-{len(self.resultats['attaques'])}"
            
            attaque = Attaque(
                payload=f"Test CSRF on {action_url}",
                date_attaque=datetime.now(),
                resultat=0,
                id_Type=3
            )
            attaque.id_provisoire = id_provisoire
            
            if not has_form_csrf and not has_global_csrf:
                logger.warning(f"[VULNÉRABLE] {url} - CSRF: POST method with sensitive fields without detectable CSRF protection")
                attaque.resultat = 1
                
                # Déterminer la gravité en fonction des champs du formulaire
                gravite = 7 if self._has_high_risk_fields(form) else 6
                
                faille = Faille(
                    gravite=gravite,
                    description=f"Form with sensitive fields without CSRF protection: {action_url}",
                    balise="form"
                )
                faille.id_provisoire = id_provisoire
                self.resultats['failles'].append(faille)
            
            self.resultats['attaques'].append(attaque)
    
    def _check_form_for_csrf(self, form):
        inputs = form.find_all("input")
        
        for inp in inputs:
            input_name = inp.get("name", "").lower()
            input_id = inp.get("id", "").lower()
            input_value = inp.get("value", "")
            
            # Vérifier les noms et IDs pour des mots-clés CSRF
            if any(keyword in input_name or keyword in input_id for keyword in self.csrf_keywords):
                # Si une valeur est fournie et qu'elle semble être un token (non vide et assez longue)
                if input_value and len(input_value) > 8:
                    return True
        
        return False
    
    def _is_search_form(self, form):
        # Détecter les formulaires de recherche simples
        search_indicators = ['search', 'find', 'query', 'lookup']
        
        # Vérifier l'action ou la classe
        form_action = form.get("action", "").lower()
        form_class = form.get("class", [])
        form_id = form.get("id", "").lower()
        
        if isinstance(form_class, list):
            form_class = " ".join(form_class).lower()
        else:
            form_class = str(form_class).lower()
            
        if any(ind in form_action or ind in form_class or ind in form_id for ind in search_indicators):
            # Vérifier le nombre de champs (formulaire de recherche typique)
            inputs = form.find_all("input")
            if len(inputs) <= 2:  # Un champ de recherche et possiblement un bouton submit
                return True
                
        return False
    
    def _has_sensitive_fields(self, form):
        sensitive_field_indicators = [
            'password', 'email', 'username', 'login', 'user', 
            'account', 'payment', 'credit', 'card', 'address', 
            'phone', 'mobile', 'profile', 'settings', 'config',
            'admin', 'create', 'delete', 'update', 'edit', 'modify'
        ]
        
        # Vérifier les noms d'entrées
        inputs = form.find_all(["input", "textarea", "select"])
        for field in inputs:
            field_name = field.get("name", "").lower()
            field_id = field.get("id", "").lower()
            field_type = field.get("type", "").lower()
            
            if field_type == "password":
                return True
                
            if any(ind in field_name or ind in field_id for ind in sensitive_field_indicators):
                return True
                
        # Vérifier l'action du formulaire
        form_action = form.get("action", "").lower()
        if any(ind in form_action for ind in ['login', 'signup', 'register', 'create', 'update', 'edit', 'admin']):
            return True
            
        return False
    
    def _has_high_risk_fields(self, form):
        high_risk_indicators = [
            'password', 'admin', 'payment', 'credit', 'card',
            'bank', 'account', 'transfer', 'delete', 'remove'
        ]
        
        inputs = form.find_all(["input", "textarea", "select"])
        for field in inputs:
            field_name = field.get("name", "").lower()
            field_id = field.get("id", "").lower()
            
            if any(ind in field_name or ind in field_id for ind in high_risk_indicators):
                return True
                
        return False
    
    def run_csrf(self, url):
        if self.test_csrf(url):
            return self.resultats
        else:
            return self.resultats