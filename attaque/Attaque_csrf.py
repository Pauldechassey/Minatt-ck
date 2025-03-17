import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


class Attaque_csrf:
    def __init__(self):
        self.results = []
        self.session = requests.Session()

    def test_csrf(self, url, timeout=10):
        vuln = False
        
        # Retrieving the CSRF token
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
        
        return len(self.results) > 0
    
    def _check_page_for_csrf_token(self, soup):
        # Looking for CSRF tokens in meta tags
        meta_csrf = soup.find('meta', attrs={'name': re.compile(r'csrf|xsrf', re.I)})
        if meta_csrf:
            return True
            
        # Looking for tokens in JavaScript variables
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and re.search(r'(csrf|xsrf).*token', script.string, re.I):
                return True
                
        return False
        
    def _analyze_forms(self, soup, url, has_csrf_token):
        forms = soup.find_all('form')
        
        for form in forms:
            action = form.get("action", "")
            if action:
                action_url = urljoin(url, action)
            else:
                action_url = url
                
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
            
            # If no CSRF token is found, the form is potentially vulnerable
            if not has_form_csrf and not has_csrf_token:
                
                self.results.append({
                    "type": "CSRF",
                    "url": url,
                    "element": f"Form targeting {action_url}",
                    "method": method,
                    "proof": "POST method without detectable CSRF protection"
                })
    
    def run_csrf(self, url):
        if self.test_csrf(url):
            print(f"CSRF vulnerability found on {url}")
            return self.results
        else:
            print(f"No CSRF vulnerability detected on {url}")
            return None

