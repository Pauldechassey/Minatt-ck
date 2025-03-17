import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie
import re
from urllib.parse import urljoin


class Attaque_headers_cookies:
    def __init__(self):
        self.results = []
        self.session = requests.Session()

    def test_headers_cookies(self, url, timeout=10):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
            return False
        
        self._analyze_headers(response, url)
        self._analyze_cookies(response, url)
        
        return len(self.results) > 0
    
    def _analyze_headers(self, response, url):
        """Check for missing or misconfigured security headers"""
        headers = response.headers
        
        # Essential security headers to check
        security_headers = {
            'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
            'X-Content-Type-Options': ['nosniff'],
            'Content-Security-Policy': None, 
            'X-XSS-Protection': ['1', '1; mode=block'],
            'Strict-Transport-Security': None,
            'Referrer-Policy': None
        }
        
        for header, valid_values in security_headers.items():
            if header not in headers:
                self.results.append({
                    "type": "Header Security",
                    "url": url,
                    "element": f"Header: {header}",
                    "proof": f"Missing security header: {header}"
                })
            elif valid_values is not None:
                header_value = headers[header].lower()
                valid = False
                for valid_value in valid_values:
                    if valid_value.lower() in header_value:
                        valid = True
                        break
                
                if not valid:
                    self.results.append({
                        "type": "Header Security",
                        "url": url,
                        "element": f"Header: {header}",
                        "proof": f"Misconfigured security header: {header}={headers[header]}"
                    })
        
        # Analyse supplémentaire pour Content-Security-Policy et Strict-Transport-Security
        if 'Content-Security-Policy' in headers:
            csp = headers['Content-Security-Policy']
            if "default-src 'self'" not in csp and "script-src 'self'" not in csp:
                self.results.append({
                    "type": "Header Security",
                    "url": url,
                    "element": "Content-Security-Policy",
                    "proof": f"Weak CSP configuration: {csp}"
                })
        
        if 'Strict-Transport-Security' in headers:
            hsts = headers['Strict-Transport-Security']
            if "max-age=" not in hsts:
                self.results.append({
                    "type": "Header Security",
                    "url": url,
                    "element": "Strict-Transport-Security",
                    "proof": f"Weak HSTS configuration: {hsts}"
                })
    
    def _analyze_cookies(self, response, url):
        # Retrieve cookies in raw format
        cookie_header = response.headers.get("Set-Cookie")
        
        if cookie_header:
            cookies = SimpleCookie()
            try:
                for header in cookie_header.split(','):
                    cookies.load(header.strip())
            except Exception:
                # Alternative method if parsing fails
                try:
                    for header in response.headers.getlist('Set-Cookie'):
                        cookies.load(header)
                except:
                    pass

            for cookie_name, cookie in cookies.items():
                # Check SameSite attribute
                samesite = None
                for attr in str(cookie).split(';'):
                    if attr.strip().lower().startswith('samesite='):
                        samesite = attr.strip().split('=')[1].lower()
                        break
                
                # Check cookie security attributes
                is_secure = 'secure' in str(cookie).lower()
                is_httponly = 'httponly' in str(cookie).lower()
                
                vulnerabilities = []
                
                if samesite is None or samesite not in ["strict", "lax"]:
                    vulnerabilities.append("SameSite missing or weak")
                
                if not is_secure:
                    vulnerabilities.append("non-secure")
                
                if not is_httponly:
                    vulnerabilities.append("non-httponly")
                
                if vulnerabilities:
                    print(f"Vulnerable cookie found: {cookie_name} - {', '.join(vulnerabilities)}")
                    self.results.append({
                        "type": "Cookie Security",
                        "url": url,
                        "element": f"Cookie: {cookie_name}",
                        "proof": f"Cookie issues: {', '.join(vulnerabilities)}"
                    })
    
    def run_headers_cookies(self, url):
        if self.test_headers_cookies(url):
            print(f"Security vulnerabilities found in headers and cookies on {url}")
            return self.results
        else:
            print(f"No security vulnerabilities detected in headers and cookies on {url}")
            return None


