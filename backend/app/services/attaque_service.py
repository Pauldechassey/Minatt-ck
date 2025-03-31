from typing import List, Dict
from app.scripts.attaque_script import AttaqueScript

def run_attack_on_urls(urls: List[str], attaque: str) -> List[Dict[str, List]]:
    attaque_service = AttaqueScript()
    all_results = []

    for url in urls:
        if attaque == "all":
            results = attaque_service.run_attack(url)
        elif attaque == "sqli":
            results = {"url": url, "sqli": attaque_service._run_sqli_scan(url)}
        elif attaque == "xss":
            results = {"url": url, "xss": attaque_service._run_xss_scan(url)}
        elif attaque == "csrf":
            results = {"url": url, "csrf": attaque_service._run_csrf_scan(url)}
        elif attaque == "headers_cookies":
            results = {"url": url, "headers_cookies": attaque_service._run_headers_cookies_scan(url)}
        else:
            results = {"url": url, "error": "Type d'attaque non valide"}
        
        all_results.append(results)

    return all_results

#probleme dans les retours... on devrait ajouter les résultats directement dans la bdd