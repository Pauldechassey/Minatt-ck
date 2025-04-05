import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from backend.app.models.attaque import Attaque
from backend.app.models.faille import Faille
from datetime import datetime


class CSRFScanner:
    def __init__(self):
        self.resultats = {
            'attaques': [],
            'failles': []
        }
        self.session = requests.Session()

    def test_csrf(self, url, timeout=10):
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        has_csrf_token = self._check_page_for_csrf_token(soup)
        self._analyze_forms(soup, url, has_csrf_token)
        
        return len(self.resultats['failles']) > 0
    
    def _check_page_for_csrf_token(self, soup):
        meta_csrf = soup.find('meta', attrs={'name': re.compile(r'csrf|xsrf', re.I)})
        if meta_csrf:
            return True
            
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and re.search(r'(csrf|xsrf).*token', script.string, re.I):
                return True
                
        return False
        
    def _analyze_forms(self, soup, url, has_csrf_token):
        forms = soup.find_all('form')
        
        for form in forms:
            action = form.get("action", "")
            action_url = urljoin(url, action) if action else url
            method = form.get("method", "GET").upper()
            
            if method != "POST":
                continue
            
            inputs = form.find_all("input")
            has_form_csrf = False
            
            csrf_keywords = ['csrf', 'xsrf', 'token', 'nonce', '_token', 'authenticity']
            
            for inp in inputs:
                input_name = inp.get("name", "").lower()
                input_id = inp.get("id", "").lower()
                
                if any(keyword in input_name or keyword in input_id for keyword in csrf_keywords):
                    has_form_csrf = True
                    break
            
            id_provisoire = f"csrf-{action_url}-{len(self.resultats['attaques'])}"

            attaque = Attaque(
                payload=f"Test CSRF on {action_url}",
                date_attaque=datetime.now(),
                resultat=0,
                id_Type=3
            )
            attaque.id_provisoire = id_provisoire


            if not has_form_csrf and not has_csrf_token:
                print(f"[VULNÉRABLE] {url} - CSRF: POST method without detectable CSRF protection")
                attaque.resultat = 1
                faille = Faille(
                    gravite=6,
                    description=f"Form without CSRF protection: {action_url}",
                    balise="form"
                )
                faille.id_provisoire = id_provisoire
                self.resultats['failles'].append(faille)
            
            self.resultats['attaques'].append(attaque)
    
    def run_csrf(self, url):
        if self.test_csrf(url):
            return self.resultats
        else:
            return self.resultats
