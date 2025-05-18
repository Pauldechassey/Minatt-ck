# FuzzCrawl Service - Web Fuzzing & Recursive Crawler

FuzzCrawl Service est une bibliothèque Python conçue pour les tests de sécurité des applications web. Elle permet d'effectuer du **fuzzing de répertoires/chemins** et un **crawling récursif** (basé sur une recherche en profondeur - DFS) afin de découvrir des ressources cachées, des liens et des vulnérabilités potentielles sur un site web cible.

La principale caractéristique de ce service est qu'il retourne les résultats sous forme d'objets Python structurés (`ScanResult` et dataclasses imbriquées), facilitant leur intégration dans d'autres applications, leur traitement pour stockage en base de données, ou leur envoi à un front-end après sérialisation.

## 🚀 Fonctionnalités

* **🌐 Fuzzing de Répertoires/Chemins :** Teste des chemins communs et personnalisés à partir d'une wordlist.
* **🕸️ Crawling Récursif :** Explore le site web en profondeur en suivant les liens découverts, jusqu'à une profondeur configurable.
* **🌲 Recherche en Profondeur (DFS) :** Méthode d'exploration privilégiée pour le crawling.
* **⚡ Support Multithreading :** Accélère les requêtes réseau pour des scans plus rapides.
* **📦 Retour d'Objets Structurés :** Renvoie les résultats sous forme d'un objet `ScanResult` contenant des dataclasses Python bien définies (`Audit`, `Domaine`, `SousDomaine`, `Attaque`, `Faille`, `TypeAttaque`).
* **👤 User-Agent Personnalisable :** (Actuellement codé en dur, mais modifiable facilement dans le script).
* **↪️ Gestion des Redirections :** Suit automatiquement les redirections HTTP.
* **🔁 Mécanisme de Réessai :** Tente à nouveau les requêtes échouées pour une meilleure robustesse.

## 📋 Prérequis

* Python 3.7 ou supérieur (en raison de l'utilisation des `dataclasses`)
* Bibliothèques Python :
  * `requests`
  * `beautifulsoup4`

Vous pouvez installer les dépendances de deux manières :

1. **Directement avec pip :**

   ```bash
   pip install requests beautifulsoup4
   ```
2. **Via un fichier `requirements.txt` :**
   Créez un fichier `requirements.txt` avec le contenu suivant :

   ```
   requests
   beautifulsoup4
   ```

   Puis exécutez :

   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Utilisation en tant que Service (Bibliothèque)

Le composant principal est la classe `FuzzerService`. Voici comment l'intégrer et l'utiliser dans votre propre code Python.

### 1. Importer les classes nécessaires

Dans votre script Python, importez la classe `FuzzerService` et la dataclass `ScanResult` (et potentiellement d'autres dataclasses si vous avez besoin d'un typage plus précis des résultats intermédiaires).

```python
# exemple_utilisation_service.py

# Assurez-vous que le fichier contenant FuzzerService (ex: fuzzer_service_tool.py)
# est dans votre PYTHONPATH ou dans le même répertoire.
from fuzzer_service_tool import FuzzerService, ScanResult

# Optionnel, pour un typage plus précis lors de l'accès aux détails des résultats :
# from fuzzer_service_tool import SousDomaine, Attaque, Faille, Audit, Domaine, TypeAttaque
  
```

### 2. Instancier FuzzerService

Créez une instance du service. Vous pouvez configurer le nombre de threads et le mode verbeux lors de l'instanciation.

```python
mon_service_fuzz = FuzzerService(threads=15, verbose=False)
Pour un logging détaillé pendant le développement/debug :
mon_service_fuzz_debug = FuzzerService(threads=5, verbose=True)
```

Chaque instance de FuzzerService est indépendante.

### 3. Appeler la méthode execute_scan

La méthode execute_scan est le point d'entrée principal. Elle prend les paramètres du scan et retourne un objet ScanResult.

```python
cible_url = "http://testphp.vulnweb.com/"
chemin_wordlist = "ma_wordlist.csv"  # Assurez-vous que ce fichier existe
profondeur_max = 2

try:
    # L'appel principal au service
    resultat_scan: ScanResult = mon_service_fuzz.execute_scan(
        base_url=cible_url,
        wordlist_path=chemin_wordlist,
        max_depth=profondeur_max
        # output_path_for_audit="audit_record.json" # Optionnel: si vous voulez que l'objet Audit contienne ce chemin
    )

    # À ce stade, resultat_scan contient toutes les données structurées du scan.
    # Vous pouvez maintenant traiter cet objet.

except FileNotFoundError:
    print(f"Erreur: Le fichier wordlist '{chemin_wordlist}' n'a pas été trouvé.")
except Exception as e:
    print(f"Une erreur inattendue est survenue durant le scan: {e}")

```

### 4. Traiter l'objet ScanResult

L'objet ScanResult retourné contient toutes les informations collectées, organisées en objets.

```python
# Suite de l'exemple précédent, en supposant que resultat_scan a été obtenu

if resultat_scan and resultat_scan.audit_info.etat == "completed":
    print(f"--- Résumé du Scan pour {resultat_scan.domaine_info.url_domaine} ---")
    print(f"ID de l'Audit: {resultat_scan.audit_info.id_audit}")
    print(f"Scan terminé le: {resultat_scan.audit_info.date_fin_audit}")
    print(f"Nombre de types d'attaques définis: {len(resultat_scan.types_attaque_info)}")

    print(f"\n--- Sous-domaines/Chemins Découverts ({len(resultat_scan.sous_domaines_info)}) ---")
    for sd in resultat_scan.sous_domaines_info:
        print(f"\n  [ID_SD: {sd.id_SD}] URL: {sd.url_SD} (Degré: {sd.degre})")
        print(f"    Description: {sd.description_SD}")

        if sd.attaques:
            print(f"    Attaques sur ce chemin ({len(sd.attaques)}):")
            for attaque in sd.attaques:
                print(f"      [ID_Attaque: {attaque.id_attaque}] Payload: '{attaque.payload}', Résultat: {attaque.resultat}")
                if attaque.failles:
                    print(f"      Failles associées ({len(attaque.failles)}):")
                    for faille in attaque.failles:
                        print(f"        [ID_Faille: {faille.id_faille}] Gravité: {faille.gravite} - {faille.description}")
                else:
                    print("        Aucune faille directe associée à cette attaque.")
        else:
            print("    Aucune attaque spécifique (fuzzing) enregistrée pour ce chemin (probablement découvert par crawling).")

        if sd.liens_internes_trouves:
            print(f"    Liens internes trouvés sur cette page ({len(sd.liens_internes_trouves)}):")
            # for lien in sd.liens_internes_trouves:
            # print(f"      - {lien}") # Décommenter pour lister tous les liens
        else:
            print("    Aucun lien interne supplémentaire trouvé sur cette page.")
else:
    if resultat_scan:
        print(f"Le scan n'a pas pu être complété. État de l'audit: {resultat_scan.audit_info.etat}")
    else:
        print("Aucun résultat de scan n'a été retourné (vérifiez les erreurs précédentes).")
```

# Structure de l'objet ScanResult et des Dataclasses

L'objet ScanResult retourné par execute_scan a la structure suivante :

```
audit_info: Audit
domaine_info: Domaine
types_attaque_info: List[TypeAttaque]
sous_domaines_info: List[SousDomaine]
```

Où chaque SousDomaine dans sous_domaines_info peut contenir :

```
attaques: List[Attaque]
```

Et chaque Attaque dans SousDomaine.attaques peut contenir :

```
failles: List[Faille]
```

Consultez le code source de fuzzer_service_tool.py pour la définition exacte des champs de chaque dataclass (Audit, Domaine, SousDomaine, Attaque, Faille, TypeAttaque).

## ⚙️ Fonctionnement Interne du Service

Le service opère en plusieurs phases (détaillées dans les commentaires du code source fuzzer_service_tool.py) :

1. Initialisation de l'état (_reset_state) : Assure que chaque appel à execute_scan est isolé.
2. Phase 1 : Fuzzing (_fuzz_urls) : Teste les chemins de la wordlist, crée des objets SousDomaine, Attaque, Faille.
3. Phase 2 : Crawling (_crawl_recursive) : Explore les liens à partir de l'URL de base et des pages fuzzed, crée ou met à jour des objets SousDomaine avec leur degre et les liens_internes_trouves.
4. Construction du résultat : Assemble tous les objets créés dans un ScanResult.

## 🧪 Exécution en Mode Standalone (pour Test)

Le script fuzzer_service_tool.py peut également être exécuté directement depuis la ligne de commande à des fins de test. Cela utilise une fonction main_standalone() qui instancie le service et appelle execute_scan.
Exemple de commande de test :

```bash
  python fuzzer_service_tool.py --url http://testphp.vulnweb.com/ --wordlist test_wordlist.csv --max-depth 2 --output test_output.json --verbose
```

Cette commande exécutera un scan et, si --output est spécifié, sauvegardera les résultats (l'objet ScanResult converti en dictionnaire) dans un fichier JSON. Cela est utile pour inspecter la structure des données retournées par le service.

```
Argument	Requis ?	Description (pour le mode standalone de test)	Défaut
--url URL	Oui	URL de base.	-
--wordlist FICHIER	Oui	Chemin wordlist CSV.	-
--output FICHIER	Non	Optionnel : Chemin pour sauvegarder le JSON de test.	-
--max-depth N	Non	Profondeur max du crawl.	3
--threads N	Non	Nombre de threads.	10
--verbose	Non	Active logging DEBUG.	-
```
