from datetime import time
from typing import Dict, List, Optional
from backend.app.scripts.sqli_script import SQLIScanner
from backend.app.scripts.xss_script import XSSScanner
from backend.app.scripts.csrf_script import CSRFScanner
from backend.app.scripts.headers_cookies_script import HeadersCookiesScanner
from backend.app.models.sous_domaine import SousDomaine
import logging
import time

logger= logging.getLogger(__name__)


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

    def run_attack(self, sous_domaine: SousDomaine, types_attaques: List[str]) -> Dict[str, List]:        
        # Initialisation du dictionnaire de résultats
        self.resultat_attaque = {
            "url": sous_domaine.url_SD,
            "sqli": [],
            "xss": [],
            "csrf": [],
            "headers_cookies": []
        }
        
        
        if types_attaques == ['all']:
            types_attaques = ["sqli", "xss", "csrf", "headers_cookies"]
            #logger.info("Option 'all' détectée - Exécution de toutes les attaques disponibles")
        
        attaques_mapping = {
            "sqli": self._run_sqli_scan,
            "xss": self._run_xss_scan,
            "csrf": self._run_csrf_scan,
            "headers_cookies": self._run_headers_cookies_scan
        }
        
        
        for type_attaque in types_attaques:
            
            if type_attaque in attaques_mapping:
                try:
                    #logger.info(f"Démarrage du scan {type_attaque} sur {sous_domaine.url_SD}")
                    debut_scan = time.time()
                    
                    self.resultat_attaque[type_attaque] = attaques_mapping[type_attaque](sous_domaine.url_SD)
                    
                    duree_scan = time.time() - debut_scan
                    #logger.info(f"Scan {type_attaque} terminé en {duree_scan:.2f} secondes")
                    
                    if self.resultat_attaque[type_attaque]:
                        for idx, vuln in enumerate(self.resultat_attaque[type_attaque]):
                            logger.debug(f"Vulnérabilité {idx+1}: {vuln}")
                    
                except Exception as e:
                    logger.error(f"Erreur lors du scan {type_attaque} : {str(e)}")
                    #logger.exception("Détails de l'erreur:")
                    self.resultat_attaque[type_attaque] = []
                    #logger.info(f"Résultat pour {type_attaque} réinitialisé à liste vide suite à l'erreur")
            else:
                logger.warning(f"Type d'attaque inconnu ignoré: {type_attaque}")
        
        #logger.info(f"Toutes les attaques terminées pour {sous_domaine.url_SD}")
    
        return self.resultat_attaque

    def _run_sqli_scan(self, url: str) -> List:
        try:
            resultats = self.sqli_scanner.run_sqli(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan SQL Injection : {e}")
            return []

    def _run_xss_scan(self, url: str) -> List:
        try:
            resultats = self.xss_scanner.run_xss(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan XSS : {e}")
            return []

    def _run_csrf_scan(self, url: str) -> List:
        try:
            resultats = self.csrf_scanner.run_csrf(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan CSRF : {e}")
            return []

    def _run_headers_cookies_scan(self, url: str) -> List:
        try:
            resultats = self.headers_cookies_scanner.run_headers_cookies(url)
            return resultats if resultats else []
        except Exception as e:
            print(f"Erreur de scan des en-têtes et cookies : {e}")
            return []


    def get_attack_results(self):
        return self.resultats_attaques

