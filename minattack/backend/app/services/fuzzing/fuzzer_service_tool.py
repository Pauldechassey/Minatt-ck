#!/usr/bin/env python3

import argparse
import datetime
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Set, Tuple, Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from sqlalchemy.orm import Session

# --- Importations des modèles SQLAlchemy de l'application ---
# SCRIPT_DIR_FTS will be .../minattack/backend/app/services/fuzzing
SCRIPT_DIR_FTS = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT_FTS should be .../Minatt-ck
# fuzzing (1) -> services (2) -> app (3) -> backend (4) -> minattack (5) -> Project Root (Minatt-ck)
PROJECT_ROOT_FTS = os.path.abspath(os.path.join(SCRIPT_DIR_FTS, '..', '..', '..', '..', '..'))
if PROJECT_ROOT_FTS not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_FTS)

# print("--- DEBUG SYS.PATH (fuzzer_service_tool) ---")
# print(f"SCRIPT_DIR_FTS: {SCRIPT_DIR_FTS}")
# print(f"PROJECT_ROOT_FTS calculé : {PROJECT_ROOT_FTS}")
# for p in sys.path:
#     print(p)
# print("--- FIN DEBUG SYS.PATH (fuzzer_service_tool) ---")

try:
    from minattack.backend.app.models.audit import Audit
    from minattack.backend.app.models.domaine import Domaine
    from minattack.backend.app.models.sous_domaine import SousDomaine
    from minattack.backend.app.models.attaque import Attaque
    from minattack.backend.app.models.faille import Faille
    from minattack.backend.app.models.type_attaque import Type_attaque as TypeAttaqueDB
    # Ensure User model is imported if Audit or other models here depend on it during initialization
    # Though ideally, models/__init__.py handles making all models known.
    from minattack.backend.app.models.user import User # Explicitly import User
    from minattack.backend.app.database import SessionLocal, engine, Base as DBBase
except ImportError as e:
    print(f"ÉCHEC de l'import avec 'minattack.backend...' dans fuzzer_service_tool.py: {e}")
    raise

if not logging.getLogger().hasHandlers(): 
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger(__name__) 

DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = "Mozilla/5.0 FuzzCrawler/1.0"
DEFAULT_THREADS = 10 
MAX_RETRIES = 3
DEFAULT_USER_ID = 1 
TYPE_ATTAQUE_FUZZING_NAME = "Directory Fuzzing"
TYPE_ATTAQUE_FUZZING_DESC = "Fuzzing for common directories and files based on wordlists."

class FuzzerService:
    def __init__(self, threads: int = DEFAULT_THREADS, verbose: bool = False):
        self.threads = threads
        self.verbose = verbose
        if verbose:
            logger.setLevel(logging.DEBUG) 

        self._reset_state() 

        self.headers = {
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def _reset_state(self):
        self.current_audit_db: Optional[Audit] = None 
        self.current_domaine_db: Optional[Domaine] = None 
        self.type_attaque_fuzzing_db: Optional[TypeAttaqueDB] = None 
        
        self.url_to_sd_db_map: Dict[str, SousDomaine] = {}
        self.visited_urls_for_processing: Set[str] = set()

        self.current_base_url_of_scan: str = "" 
        self.current_domain_netloc_of_scan: str = "" 
        self.max_depth_of_scan: int = 0


    def initialize_scan_session(self, db: Session, domaine_db: Domaine, base_scan_url: str, max_depth_scan: int):
        self._reset_state() 
        self.current_domaine_db = domaine_db
        self.type_attaque_fuzzing_db = self._get_or_create_type_attaque(db, TYPE_ATTAQUE_FUZZING_NAME, TYPE_ATTAQUE_FUZZING_DESC)
        self.current_base_url_of_scan = base_scan_url.rstrip("/")
        self.current_domain_netloc_of_scan = urlparse(self.current_base_url_of_scan).netloc
        self.max_depth_of_scan = max_depth_scan
        logger.debug(f"FuzzerService initialized for domain {domaine_db.url_domaine}, scan base {base_scan_url}, max_depth {max_depth_scan}")

    def _get_current_timestamp_dt(self) -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    def _get_or_create_type_attaque(self, db: Session, nom_type: str, description_type: str) -> TypeAttaqueDB:
        type_attaque_obj = db.query(TypeAttaqueDB).filter_by(nom_type=nom_type).first()
        if not type_attaque_obj:
            logger.info(f"Fuzzer: Création du Type_attaque '{nom_type}' en BDD.")
            type_attaque_obj = TypeAttaqueDB(
                nom_type=nom_type,
                description_type=description_type
            )
            db.add(type_attaque_obj)
            db.flush() 
        return type_attaque_obj

    def _get_or_create_sous_domaine(self, db: Session, url: str, description: str, degre: int, fk_id_sd_parent: Optional[int] = None) -> Optional[SousDomaine]:
        normalized_url = url.rstrip('/')
        
        # Check internal map first
        if normalized_url in self.url_to_sd_db_map:
            sd_obj = self.url_to_sd_db_map[normalized_url]
            if degre < sd_obj.degre: # If found via a shorter path
                sd_obj.degre = degre
                # The attribute for parent in your SousDomaine model is id_SD_Sous_domaine
                if fk_id_sd_parent and sd_obj.id_SD_Sous_domaine is None : 
                    sd_obj.id_SD_Sous_domaine = fk_id_sd_parent
            return sd_obj

        if not self.current_domaine_db:
            logger.error("Fuzzer: current_domaine_db non défini. Appelez initialize_scan_session d'abord.")
            return None

        # Query existing SousDomaine from DB using the CORRECT column/attribute name 'id_domaine'
        sd_obj = db.query(SousDomaine).filter_by(
            url_SD=normalized_url, 
            id_domaine=self.current_domaine_db.id_domaine # <<< THIS IS THE KEY CHANGE (was id_domaine)
        ).first()

        if sd_obj:
            logger.debug(f"Fuzzer: SousDomaine {normalized_url} trouvé en BDD (ID: {sd_obj.id_SD}).")
            # Update if found via a shorter path or new parent
            if degre < sd_obj.degre:
                sd_obj.degre = degre
            # The attribute for parent in your SousDomaine model is id_SD_Sous_domaine
            if fk_id_sd_parent and sd_obj.id_SD_Sous_domaine is None: # Only set parent if not already set
                 sd_obj.id_SD_Sous_domaine = fk_id_sd_parent
            self.url_to_sd_db_map[normalized_url] = sd_obj # Add to current scan's map
            return sd_obj
        
        # Create new SousDomaine if not found
        logger.debug(f"Fuzzer: Création du SousDomaine {normalized_url} (degre {degre}) en BDD.")
        sd_obj = SousDomaine(
            url_SD=normalized_url,
            description_SD=description,
            degre=degre,
            id_domaine=self.current_domaine_db.id_domaine, # <<< USE CORRECT ATTRIBUTE NAME HERE
            # The attribute for parent in your SousDomaine model is id_SD_Sous_domaine
            id_SD_Sous_domaine=fk_id_sd_parent 
        )
        db.add(sd_obj)
        db.flush() 
        self.url_to_sd_db_map[normalized_url] = sd_obj 
        return sd_obj

    def load_wordlist(self, wordlist_path: str) -> List[str]:
        import csv
        try:
            # SCRIPT_DIR_FTS is .../app/services/fuzzing/
            if not os.path.isabs(wordlist_path):
                path_to_load = os.path.join(SCRIPT_DIR_FTS, wordlist_path)
            else:
                path_to_load = wordlist_path
            
            if not os.path.isfile(path_to_load):
                logger.error(f"Fuzzer: Wordlist file not found: {path_to_load}")
                raise FileNotFoundError(f"Fuzzer: Wordlist file not found: {path_to_load}")

            words = []
            with open(path_to_load, "r", newline="", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row and len(row) > 0 and row[0].strip():
                        words.append(row[0].strip())
        
            logger.debug(f"Fuzzer: Loaded {len(words)} words from CSV wordlist {path_to_load}")
            return words
        except Exception as e:
            logger.error(f"Fuzzer: Error loading CSV wordlist {wordlist_path}: {e}")
            raise

    def fetch_url(self, url: str) -> Tuple[str, Optional[requests.Response]]:
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    timeout=DEFAULT_TIMEOUT,
                    allow_redirects=True
                )
                final_url = response.url.rstrip('/')
                return final_url, response
            except RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    logger.debug(f"Fuzzer: Failed to fetch {url} after {MAX_RETRIES} attempts: {e}")
                    return url.rstrip('/'), None
                time.sleep(1) 
        return url.rstrip('/'), None


    def extract_links(self, page_url: str, response: requests.Response) -> List[str]:
        links = []
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"].strip()
                if href and not href.startswith(("#", "javascript:", "mailto:", "tel:")):
                    absolute_url = urljoin(page_url, href).rstrip('/') 
                    if urlparse(absolute_url).netloc == self.current_domain_netloc_of_scan:
                        links.append(absolute_url)
        except Exception as e:
            logger.debug(f"Fuzzer: Error extracting links from {page_url}: {e}")
        return list(set(links))


    def _process_url_discovery(self, db: Session, url_to_process: str, depth: int, 
                               is_fuzzed_path: bool = False, payload: Optional[str] = None,
                               fk_id_sd_parent: Optional[int] = None) -> Tuple[Optional[SousDomaine], List[str]]:
        normalized_url = url_to_process.rstrip('/')
        extracted_links: List[str] = []

        if normalized_url in self.visited_urls_for_processing and not is_fuzzed_path:
            sd_existing_check = self.url_to_sd_db_map.get(normalized_url)
            return sd_existing_check, []

        fetched_url, response = self.fetch_url(normalized_url)

        if fetched_url != normalized_url:
            logger.debug(f"Fuzzer: URL {normalized_url} redirected to {fetched_url}")
            if fetched_url in self.url_to_sd_db_map: 
                 existing_sd = self.url_to_sd_db_map[fetched_url]
                 if depth < existing_sd.degre:
                     existing_sd.degre = depth
                 return existing_sd, []
            normalized_url = fetched_url

        self.visited_urls_for_processing.add(normalized_url) 

        if not response or response.status_code != 200:
            if is_fuzzed_path and response is not None : 
                 logger.info(f"Fuzzer: Fuzzed path {normalized_url} (Payload: {payload}) resulted in status {response.status_code}.")
            else:
                logger.debug(f"Fuzzer: URL {normalized_url} inaccessible (Status: {response.status_code if response else 'N/A'}).")
            return None, []

        description_sd = "Discovered by Fuzzing" if is_fuzzed_path else "Discovered by Crawling (via Fuzzer methods)"
        sd_obj = self._get_or_create_sous_domaine(db, normalized_url, description_sd, depth, fk_id_sd_parent)
        
        if not sd_obj:
            return None, []

        if "text/html" in response.headers.get("Content-Type", "").lower():
            extracted_links = self.extract_links(normalized_url, response) 

        if is_fuzzed_path and payload:
            if not self.type_attaque_fuzzing_db:
                logger.error("Fuzzer: TypeAttaque pour Fuzzing non initialisé. Appelez initialize_scan_session.")
                return sd_obj, extracted_links

            existing_attack = db.query(Attaque).filter_by(
                id_SD=sd_obj.id_SD,
                payload=payload,
                id_Type=self.type_attaque_fuzzing_db.id_Type
            ).first()

            if not existing_attack:
                logger.info(f"Fuzzer: Enregistrement Attaque Fuzzing pour SD ID {sd_obj.id_SD}, URL {sd_obj.url_SD}, Payload {payload}")
                new_attaque = Attaque(
                    payload=payload,
                    date_attaque=self._get_current_timestamp_dt(),
                    resultat=1, 
                    id_SD=sd_obj.id_SD, 
                    id_Type=self.type_attaque_fuzzing_db.id_Type 
                )
                db.add(new_attaque)
                db.flush() 

                new_faille = Faille(
                    gravite="Information", 
                    description=f"Accessible path found via directory fuzzing: {sd_obj.url_SD} (Status: {response.status_code})",
                    balise=payload, 
                    id_attaque=new_attaque.id_attaque 
                )
                db.add(new_faille)
                db.flush() 
            else:
                logger.debug(f"Fuzzer: Attaque Fuzzing avec payload {payload} existe déjà pour SD ID {sd_obj.id_SD}.")
        
        return sd_obj, extracted_links

    def fuzz_single_url_paths(self, db: Session, base_fuzz_url_sd_obj: SousDomaine, wordlist: List[str]) -> Tuple[List[SousDomaine], List[Tuple[SousDomaine, List[str]]]]:
        if not self.current_domaine_db or not self.type_attaque_fuzzing_db:
            logger.error("Fuzzer: Service non initialisé. Appelez initialize_scan_session d'abord.")
            return [], []

        logger.info(f"Fuzzer: Starting fuzzing on base URL: {base_fuzz_url_sd_obj.url_SD} (Depth of base SD: {base_fuzz_url_sd_obj.degre})")
        
        discovered_sds_from_fuzz: List[SousDomaine] = []
        fuzzed_pages_with_their_links: List[Tuple[SousDomaine, List[str]]] = []

        fuzz_tasks_args = []
        for word in wordlist:
            path_segment = word.strip('/')
            if not path_segment: 
                continue
            url_to_test = urljoin(base_fuzz_url_sd_obj.url_SD.rstrip('/') + '/', path_segment)
            fuzz_tasks_args.append({
                "url_to_test": url_to_test, 
                "word": word
            })

        with ThreadPoolExecutor(max_workers=self.threads, thread_name_prefix="FuzzerPath") as executor:
            futures = [
                executor.submit(
                    self._process_url_discovery, 
                    db, 
                    args["url_to_test"], 
                    base_fuzz_url_sd_obj.degre + 1, 
                    is_fuzzed_path=True, 
                    payload=args["word"],
                    fk_id_sd_parent=base_fuzz_url_sd_obj.id_SD 
                ) for args in fuzz_tasks_args
            ]

            for future in futures:
                try:
                    sd_obj, extracted_links = future.result()
                    if sd_obj: 
                        if sd_obj not in discovered_sds_from_fuzz: 
                             discovered_sds_from_fuzz.append(sd_obj)
                        if extracted_links: 
                            fuzzed_pages_with_their_links.append((sd_obj, extracted_links))
                except Exception as e:
                    logger.error(f"Fuzzer: Error during a fuzzing task processing: {e}", exc_info=self.verbose)
        
        logger.info(f"Fuzzer: Fuzzing on {base_fuzz_url_sd_obj.url_SD} complete. {len(discovered_sds_from_fuzz)} new/updated SousDomaines from fuzzing. {len(fuzzed_pages_with_their_links)} fuzzed pages yielded further links.")
        return discovered_sds_from_fuzz, fuzzed_pages_with_their_links


    # --- Standalone Execution Part ---
    def _crawl_recursive(self, db: Session, url: str, depth: int, wordlist: List[str], parent_sd_id: Optional[int] = None):
        normalized_url = url.rstrip('/')
        if depth > self.max_depth_of_scan: 
            return

        if normalized_url in self.visited_urls_for_processing: 
             existing_sd = self.url_to_sd_db_map.get(normalized_url)
             if existing_sd and existing_sd.degre <= depth:
                logger.debug(f"Fuzzer CRAWL (standalone): URL {normalized_url} (depth {depth}) already processed at depth {existing_sd.degre}. Skipping.")
                return
        
        logger.info(f"Fuzzer CRAWL (standalone): {normalized_url} (Depth: {depth})")
        
        sd_obj, links_found_on_page = self._process_url_discovery(db, normalized_url, depth, is_fuzzed_path=False, fk_id_sd_parent=parent_sd_id)

        if not sd_obj: 
            return
        
        _, fuzzed_pages_and_links = self.fuzz_single_url_paths(db, sd_obj, wordlist)
        
        new_links_to_crawl_from_fuzz = []
        for fuzzed_sd, links_on_fuzzed in fuzzed_pages_and_links:
            if fuzzed_sd.degre < self.max_depth_of_scan: 
                for link in links_on_fuzzed:
                    new_links_to_crawl_from_fuzz.append((link, fuzzed_sd.degre + 1, fuzzed_sd.id_SD))
        
        all_links_to_consider = []
        for link in links_found_on_page: 
             all_links_to_consider.append((link, depth + 1, sd_obj.id_SD))
        all_links_to_consider.extend(new_links_to_crawl_from_fuzz)


        if depth < self.max_depth_of_scan: # This check might be redundant if fuzzed_sd.degre check is robust
            for link_url, link_depth, link_parent_id in all_links_to_consider:
                # Ensure link_depth itself does not exceed max_depth_of_scan
                if link_depth <= self.max_depth_of_scan:
                    self._crawl_recursive(db, link_url, link_depth, wordlist, link_parent_id)


    def execute_scan_standalone(self, db: Session, target_url: str, wordlist_path: str, max_depth: int, user_id: int, path_rapport_audit: Optional[str] = None) -> Optional[Audit]:
        start_time = time.time()
        
        domaine_obj = db.query(Domaine).filter_by(url_domaine=target_url.rstrip("/")).first()
        if not domaine_obj:
            logger.info(f"Fuzzer STANDALONE: Création du Domaine {target_url.rstrip('/')} en BDD.")
            domaine_obj = Domaine(
                url_domaine=target_url.rstrip("/"),
                description_domaine=f"Scan target: {target_url.rstrip('/')}"
            )
            db.add(domaine_obj)
            db.flush()
        else:
            logger.info(f"Fuzzer STANDALONE: Utilisation du Domaine existant {domaine_obj.url_domaine} (ID: {domaine_obj.id_domaine}).")

        self.initialize_scan_session(db, domaine_obj, target_url, max_depth)

        logger.info(f"Fuzzer STANDALONE: Création de l'Audit pour le Domaine ID {self.current_domaine_db.id_domaine}.")
        self.current_audit_db = Audit(
            date_debut_audit=self._get_current_timestamp_dt(),
            id_user=user_id,
            id_domaine=self.current_domaine_db.id_domaine, 
            etat="running",
            path_rapport=path_rapport_audit
        )
        db.add(self.current_audit_db)
        db.flush()

        logger.info(f"Fuzzer STANDALONE: Début du scan pour {self.current_base_url_of_scan} (Audit ID: {self.current_audit_db.id_audit})")

        try:
            wordlist = self.load_wordlist(wordlist_path)
        except FileNotFoundError:
            logger.error(f"Fuzzer STANDALONE: Wordlist non trouvée à {wordlist_path}. Arrêt du scan.")
            if self.current_audit_db:
                self.current_audit_db.etat = "error_wordlist_not_found"
                self.current_audit_db.date_fin_audit = self._get_current_timestamp_dt()
            db.commit() 
            return self.current_audit_db

        logger.info(f"Fuzzer STANDALONE: Démarrage du crawl récursif et fuzzing intégré depuis la base.")
        self._crawl_recursive(db, self.current_base_url_of_scan, 0, wordlist, parent_sd_id=None)


        if self.current_audit_db:
            self.current_audit_db.etat = "completed"
            self.current_audit_db.date_fin_audit = self._get_current_timestamp_dt()
        
        db.commit() 
        
        elapsed_time = time.time() - start_time
        logger.info(f"Fuzzer STANDALONE: Scan terminé en {elapsed_time:.2f} secondes.")
        logger.info(f"Fuzzer STANDALONE: Nombre total d'URLs pour lesquelles un fetch a été tenté: {len(self.visited_urls_for_processing)}")
        logger.info(f"Fuzzer STANDALONE: Nombre de SousDomaines uniques (créés/mis à jour) dans ce scan: {len(self.url_to_sd_db_map)}")

        return self.current_audit_db


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Web Fuzzing & Recursive Crawler - Service (Standalone Test)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--url", required=True, help="Base URL de la cible")
    parser.add_argument("--wordlist", required=True, help="Chemin vers la wordlist CSV (relatif à ce script si non absolu)")
    parser.add_argument("--max-depth", type=int, default=1, help="Profondeur maximale du crawl")
    parser.add_argument("--output", help="Optionnel: Nom de fichier rapport")
    parser.add_argument("--threads", type=int, default=DEFAULT_THREADS, help="Nombre de threads")
    parser.add_argument("--verbose", action="store_true", help="Activer logging DEBUG")
    parser.add_argument("--user-id", type=int, default=DEFAULT_USER_ID, help="ID de l'utilisateur")
    return parser.parse_args()

def main_standalone():
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG) 
        logger.setLevel(logging.DEBUG) 
    else:
        logging.getLogger().setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

    try:
        if 'DBBase' not in globals() or DBBase is None :
             logger.critical("Les modèles de base de données n'ont pas pu être importés. Impossible de continuer.")
             sys.exit(1)
        DBBase.metadata.create_all(bind=engine) 
        logger.info("Tables de base de données vérifiées/créées (standalone).")
    except Exception as e:
        logger.error(f"Erreur lors de la création des tables (standalone): {e}", exc_info=args.verbose)
        sys.exit(1)

    db_session: Optional[Session] = None
    try:
        db_session = SessionLocal()
        logger.info("Session de base de données créée (standalone).")

        service = FuzzerService(threads=args.threads, verbose=args.verbose)
        
        audit_result_obj = service.execute_scan_standalone(
            db=db_session,
            target_url=args.url,
            wordlist_path=args.wordlist,
            max_depth=args.max_depth,
            user_id=args.user_id,
            path_rapport_audit=args.output
        )
        
        if audit_result_obj:
            print("\n--- Scan Summary (Standalone Fuzzer) ---")
            # Refresh object from session to get latest data if it was committed by service
            db_session.refresh(audit_result_obj)
            if audit_result_obj.domaine: db_session.refresh(audit_result_obj.domaine)

            print(f"Audit ID: {audit_result_obj.id_audit}, Status: {audit_result_obj.etat}")
            if audit_result_obj.domaine:
                 print(f"Domaine: {audit_result_obj.domaine.url_domaine} (ID: {audit_result_obj.domaine.id_domaine})")
            
            if db_session and audit_result_obj.domaine:
                sds_count = db_session.query(SousDomaine).filter_by(id_domaine=audit_result_obj.id_domaine).count()
                print(f"Total Sous-domaines enregistrés pour ce domaine: {sds_count}")
                
                attaques_count = db_session.query(Attaque)\
                    .join(SousDomaine, Attaque.id_SD == SousDomaine.id_SD)\
                    .filter(SousDomaine.id_domaine == audit_result_obj.id_domaine)\
                    .count()
                print(f"Total Attaques enregistrées pour ce domaine: {attaques_count}")

                failles_count = db_session.query(Faille)\
                    .join(Attaque, Faille.id_attaque == Attaque.id_attaque)\
                    .join(SousDomaine, Attaque.id_SD == SousDomaine.id_SD)\
                    .filter(SousDomaine.id_domaine == audit_result_obj.id_domaine)\
                    .count()
                print(f"Total Failles enregistrées pour ce domaine: {failles_count}")

            if args.output:
                print(f"Le chemin du rapport '{args.output}' a été enregistré dans l'audit.")
                try:
                    report_file_path = args.output
                    if not os.path.isabs(args.output):
                        report_file_path = os.path.join(os.getcwd(), args.output)

                    with open(report_file_path, "w", encoding="utf-8") as f_report:
                        f_report.write(f"Rapport d'audit (standalone fuzzer) pour le scan du {audit_result_obj.date_debut_audit}\n")
                        f_report.write(f"Audit ID: {audit_result_obj.id_audit}\n")
                        f_report.write(f"Cible: {audit_result_obj.domaine.url_domaine}\n")
                        f_report.write(f"Statut: {audit_result_obj.etat}\n")
                        f_report.write(f"Terminé le: {audit_result_obj.date_fin_audit}\n")
                    logger.info(f"Fichier de rapport simple créé : {report_file_path}")
                except Exception as e_report:
                    logger.error(f"Impossible de créer le fichier de rapport simple : {e_report}")
            print("--------------------")
        else:
            print("Le scan standalone n'a pas pu démarrer ou a échoué très tôt.")

    except KeyboardInterrupt:
        logger.warning("Opération interrompue par l'utilisateur (standalone).")
        if db_session: 
            db_session.rollback()
            # Check if service and current_audit_db exist before trying to access them
            service_exists = 'service' in locals() and hasattr(locals()['service'], 'current_audit_db')
            if service_exists and locals()['service'].current_audit_db:
                try:
                    audit_to_update = db_session.query(Audit).filter_by(id_audit=locals()['service'].current_audit_db.id_audit).first()
                    if audit_to_update:
                        audit_to_update.etat = "interrupted"
                        audit_to_update.date_fin_audit = datetime.datetime.now(datetime.timezone.utc)
                        db_session.commit()
                        logger.info("Audit status updated to 'interrupted'.")
                except Exception as e_interrupt_commit:
                    logger.error(f"Error updating audit to 'interrupted': {e_interrupt_commit}")
                    db_session.rollback()
    except Exception as e:
        logger.error(f"Erreur inattendue dans main_standalone: {e}", exc_info=args.verbose)
        if db_session:
            db_session.rollback()
    finally:
        if db_session:
            db_session.close()
            logger.info("Session de base de données fermée (standalone).")

if __name__ == "__main__":
    try:
        if 'DBBase' not in globals() or DBBase is None:
            raise ImportError("DBBase not loaded or SQLAlchemy models failed to import.")
    except ImportError as e:
        print(f"CRITICAL: Échec de l'importation des modules SQLAlchemy dans __main__ (fuzzer_service_tool.py): {e}")
        sys.exit(1)
    
    main_standalone()