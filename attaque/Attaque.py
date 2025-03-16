from Attaque_sqli import Attaque_sqli
from Attaque_xss import Attaque_xss
from Attaque_csrf import Attaque_csrf

class Attaque:
    def __init__(self):
        self.resultats_attaques = {
            "sqli": [],
            "xss": [],
            "csrf": []
        }
        
    def attaque_sqli(self, url):
        scanner = Attaque_sqli()
        resultats = scanner.run_sqli(url)
        return resultats if resultats else []
    
    def attaque_xss(self, url):
        scanner = Attaque_xss()
        resultats = scanner.run_xss(url)
        return resultats if resultats else []
    
    def attaque_csrf(self, url):
        scanner = Attaque_csrf()
        resultats = scanner.run_csrf(url)
        return resultats if resultats else []
     

    def get_resultats(self):
        return self.resultats_attaques

if __name__ == "__main__":
    """
    pour lancer le serveur :> python test_state/test_vuln.py
    -> http://127.0.0.1:5000

    """
    urls_test = [
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5000/echo",
        "http://127.0.0.1:5000/recherche",
        "http://127.0.0.1:5000/login",
        "http://127.0.0.1:5000/comments",
        "http://127.0.0.1:5000/profile"
    ]
    attaque = Attaque()
    for url in urls_test:
        print("-----------------------------------------------------------")
        print(f"test sur {url}")
        print("-------------------------")
        #attaque.resultats_attaques["sqli"].append(attaque.attaque_sqli(url))
        #attaque.resultats_attaques["xss"].append(attaque.attaque_xss(url))
        attaque.resultats_attaques["csrf"].append(attaque.attaque_csrf(url))



"""
stored xss -> ne marche pas (page comments)
sqli -> à améliorer : ne remarque pas le problème sur login
"""