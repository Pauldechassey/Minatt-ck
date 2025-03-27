from typing import Dict, List, Optional
from backend.app.scripts.sqli_script import SQLIScanner
from backend.app.scripts.xss_script import XSSScanner
from backend.app.scripts.csrf_script import CSRFScanner
from backend.app.scripts.headers_cookies_script import HeadersCookiesScanner

class AttaqueScript:
    def __init__(self):
        self.resultats_attaques = {
            "url": None,
            "sqli": [],
            "xss": [],
            "csrf": [],
            "headers_cookies": []
        }
        
        self.sqli_scanner = SQLIScanner()
        self.xss_scanner = XSSScanner()
        self.csrf_scanner = CSRFScanner()
        self.headers_cookies_scanner = HeadersCookiesScanner()

    def run_attack(self, url: str) -> Dict[str, List]:
        self.resultats_attaques = {
            "url": url,
            "sqli": [],
            "xss": [],
            "csrf": [],
            "headers_cookies": []
        }
        
        self.resultats_attaques["sqli"] = self._run_sqli_scan(url)
        self.resultats_attaques["xss"] = self._run_xss_scan(url)
        self.resultats_attaques["csrf"] = self._run_csrf_scan(url)
        self.resultats_attaques["headers_cookies"] = self._run_headers_cookies_scan(url)
        
        return self.resultats_attaques

    def _run_sqli_scan(self, url: str) -> List:
        """Effectue un scan d'injection SQL"""
        try:
            resultats = self.sqli_scanner.run_sqli(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan SQL Injection : {e}")
            return []

    def _run_xss_scan(self, url: str) -> List:
        """Effectue un scan XSS"""
        try:
            resultats = self.xss_scanner.run_xss(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan XSS : {e}")
            return []

    def _run_csrf_scan(self, url: str) -> List:
        """Effectue un scan CSRF"""
        try:
            resultats = self.csrf_scanner.run_csrf(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan CSRF : {e}")
            return []

    def _run_headers_cookies_scan(self, url: str) -> List:
        """Effectue un scan des en-têtes et cookies"""
        try:
            resultats = self.headers_cookies_scanner.run_headers_cookies(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan des en-têtes et cookies : {e}")
            return []

    def get_attack_results(self):
        return self.resultats_attaques

def run_attack_on_urls(urls: List[str]) -> List[Dict[str, List]]:
    """
    Fonction utilitaire pour exécuter des attaques sur plusieurs URLs
    
    :param urls: Liste des URLs à scanner
    :return: Liste des résultats d'attaque pour chaque URL
    """
    attaque_service = AttaqueScript()
    all_results = []
    
    for url in urls:
        print("-----------------------------------------------------------")
        print(f"Scan de {url}")
        print("-----------------------------------------------------------")
        
        results = attaque_service.run_attack(url)
        all_results.append(results)
    
    return all_results

# Exemple d'utilisation
if __name__ == "__main__":
    urls_test = [
        # "http://127.0.0.1:5000",
        # "http://127.0.0.1:5000/echo",
    ]
    
    # Exécution des attaques sur les URLs de test
    resultats = run_attack_on_urls(urls_test)
    
    for resultat in resultats:
        print(resultat)