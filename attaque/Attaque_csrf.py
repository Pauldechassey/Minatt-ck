import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie

class Attaque_csrf:
    def __init__(self):
        self.results = []
        self.session = requests.Session()

    def test_csrf(self, url):
        """Teste la vulnérabilité CSRF sur l'URL donnée."""
        vuln = False
        
        # Récupération du token CSRF
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Lève une exception si le code de status n'est pas 200
        except requests.RequestException as e:
            print(f"CSRF: Erreur lors de l'accès à {url}: {e}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # -- Vérification des formulaires --
        forms = soup.find_all('form')
        for i, form in enumerate(forms):
            action = form.get("action", "")
            method = form.get("method", "GET").upper()
            
            inputs = form.find_all("input")
            if any("csrf" in (inp.get("name", "") + inp.get("id", "")).lower() for inp in inputs) and method == "POST":
                print(f"Formulaire vulnérable trouvé: {action}")
                
                self.results.append({
                    "type": "CSRF",
                    "url": url,
                    "proof": "méthode POST sans token CSRF"
                })
                vuln = True

        # -- Vérification des cookies --
        # Récupérer les cookies en format brut
        cookie_header = response.headers.get("Set-Cookie")
        
        if cookie_header:
            cookies = SimpleCookie()
            for header in cookie_header.split(','):
                cookies.load(header.strip())
            
            for cookie_name, cookie in cookies.items():
                # Vérifier l'attribut SameSite
                samesite = None
                for attr in cookie['set-cookie'].split(';'):
                    if attr.strip().startswith('samesite='):
                        samesite = attr.strip().split('=')[1].lower()
                if samesite is not None and samesite not in ["strict", "lax"]:
                    print(f"Cookie vulnérable trouvé: {cookie_name} avec SameSite = {samesite}")
                    self.results.append({
                        "type": "CSRF",
                        "url": url,
                        "proof": f"cookie {cookie_name} avec SameSite = {samesite}"
                    })
                    vuln = True
        
        return vuln
    
    def run_csrf(self, url):
        if self.test_csrf(url):
            print(f"Vulnérabilité CSRF trouvée sur {url}")
            return self.results
        else:
            return None
