from collections import deque
import os 
import sys 
import datetime 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import re

from sqlalchemy.orm import Session
from typing import List, Set, Dict, Optional

# --- Path Setup for Imports ---
# cartographie_script.py is in .../minattack/backend/app/scripts/
SCRIPT_DIR_CS = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT_CS should be Minatt-ck
# scripts (1) -> app (2) -> backend (3) -> minattack (4) -> Project Root (Minatt-ck)
PROJECT_ROOT_CS = os.path.abspath(os.path.join(SCRIPT_DIR_CS, '..', '..', '..', '..'))

if PROJECT_ROOT_CS not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_CS)

# print("--- DEBUG SYS.PATH (cartographie_script) ---")
# print(f"SCRIPT_DIR_CS: {SCRIPT_DIR_CS}")
# print(f"PROJECT_ROOT_CS calculé : {PROJECT_ROOT_CS}")
# for p_cs in sys.path:
#     print(p_cs)
# print("--- FIN DEBUG SYS.PATH (cartographie_script) ---")


try:
    from minattack.backend.app.models.domaine import Domaine
    from minattack.backend.app.models.sous_domaine import SousDomaine
    from minattack.backend.app.models.technologie import Technologie
    # Ensure User model is imported so SQLAlchemy knows about it when Audit model is processed
    from minattack.backend.app.models.user import User 
    
    # Relative import for FuzzerService
    # from .../app/scripts/ to .../app/services/fuzzing/
    # .. goes to app/
    # then services.fuzzing
    from ..services.fuzzing.fuzzer_service_tool import FuzzerService, TYPE_ATTAQUE_FUZZING_NAME, TYPE_ATTAQUE_FUZZING_DESC
except ImportError as e:
    print(f"ImportError in cartographie_script.py: {e}")
    print("Ensure 'Minatt-ck' is in PYTHONPATH, or run from a context where 'minattack' package is discoverable.")
    print("Also ensure required __init__.py files exist in 'scripts', 'services', and 'services/fuzzing'.")
    raise


import logging

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger(__name__)


class WebCrawler:
    def __init__(self, base_url_str: str, domaine_obj: Domaine, 
                 max_depth: int = 3, 
                 wordlist_name: str = "chemins.csv", 
                 fuzzer_threads: int = 5, verbose_fuzzer: bool = False):
        
        self.base_url_str = base_url_str.rstrip('/') 
        self.domaine_model = domaine_obj 
        self.max_depth = max_depth
        
        self.sous_domaines_crawler_map: Dict[str, SousDomaine] = {} 
        self.technologies: List[Technologie] = []
        
        self.visited_urls_crawler: Set[str] = set() 
        self.queued_urls_crawler: Set[str] = set() 

        self.fuzzer = FuzzerService(threads=fuzzer_threads, verbose=verbose_fuzzer)
        self.wordlist_name = wordlist_name 
        self.wordlist_content: Optional[List[str]] = None

        if verbose_fuzzer: 
            logger.setLevel(logging.DEBUG)


    def is_internal_link(self, url_to_check: str):
        try:
            return urlparse(url_to_check).netloc == urlparse(self.base_url_str).netloc
        except Exception:
            return False

    def normalize_url(self, url: str):
        try:
            decoded_url = unquote(url)
            parsed = urlparse(decoded_url)
            
            path = parsed.path if parsed.path else '/'
            query_string = parsed.query 

            normalized = f"{parsed.scheme}://{parsed.netloc}{path}"
            if query_string:
                normalized += f"?{query_string}"
            # Normalize trailing slash: only for root, or if path itself ends with slash before query
            if normalized.endswith('/') and len(urlparse(normalized).path) > 1:
                 if not path.endswith('/') and path != '/': # if original path didn't end with / (and not root)
                    normalized = normalized.rstrip('/')
            elif not normalized.endswith('/') and path.endswith('/'): # if original path ended with /
                 if parsed.query: # if query, slash was before query
                     normalized = f"{parsed.scheme}://{parsed.netloc}{path}" + (f"?{query_string}" if query_string else "")
                 else: # no query, ensure slash
                     normalized = f"{parsed.scheme}://{parsed.netloc}{path}"


            return normalized
        except Exception:
            logger.warning(f"Error normalizing URL: {url}, returning as is (rstripped).")
            return url.rstrip('/')

    def should_crawl_url(self, url: str, current_depth: int) -> bool: 
        if current_depth > self.max_depth:
            return False

        unwanted_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.css', '.js', 
                               '.xml', '.json', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot',
                               '.mp4', '.mp3', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                               '.gz', '.tar', '.tgz', '.rar', '.iso', '.dmg', '.exe', '.msi', '.swf']

        if not self.is_internal_link(url): # URL should be normalized before this call
            return False
        
        path_part = urlparse(url).path.lower()
        if any(path_part.endswith(ext) for ext in unwanted_extensions):
            return False
        
        if url in self.visited_urls_crawler:
            if url in self.sous_domaines_crawler_map and self.sous_domaines_crawler_map[url].degre <= current_depth:
                return False 
        
        # if url in self.queued_urls_crawler: # This check might be too restrictive if re-evaluating paths
        #     return False
            
        return True


    def extract_links(self, soup: BeautifulSoup, current_page_url: str) -> Set[str]:
        links = set()
        for link_tag in soup.find_all(['a', 'link'], href=True): 
            try:
                href = link_tag.get('href')
                if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                    continue

                full_url = urljoin(current_page_url, href)
                normalized_link = self.normalize_url(full_url) 

                if self.is_internal_link(normalized_link):
                    path_part = urlparse(normalized_link).path.lower()
                    unwanted_static = ['.jpg','.jpeg','.png','.gif','.css','.js','.zip','.pdf'] 
                    if not any(path_part.endswith(ext) for ext in unwanted_static):
                        links.add(normalized_link)
            except Exception as e:
                logger.error(f"Crawler: Error extracting or normalizing link '{href}' from {current_page_url}: {e}")
        return links

    def extract_technologies(self, soup: BeautifulSoup, response: Optional[requests.Response]=None) -> List[Technologie]:
        tech_patterns = { 
            'PHP': (re.compile(r'php|index\.php|\.php([?#]|$)', re.I), re.compile(r'x-powered-by:.*?php', re.I)),
            'ASP.NET': (re.compile(r'asp\.net|\.aspx([?#]|$)', re.I), re.compile(r'x-aspnet-version|x-powered-by:.*?asp\.net', re.I)),
            'Apache': (None, re.compile(r'server:.*?apache', re.I)),
            'Nginx': (None, re.compile(r'server:.*?nginx', re.I)),
            'IIS': (None, re.compile(r'server:.*?microsoft-iis', re.I)),
            'jQuery': (re.compile(r'jquery([.-][\d\.]+)?(\.min)?\.js', re.I), None),
            'React': (re.compile(r'react([.-][\d\.]+)?(\.min)?\.js|react-dom', re.I), None),
            'Vue.js': (re.compile(r'vue([.-][\d\.]+)?(\.min)?\.js', re.I), None),
            'AngularJS': (re.compile(r'angular([.-][\d\.]+)?(\.min)?\.js', re.I), None), 
            'Angular': (re.compile(r'ngreflect|ng-version',re.I), None), 
            'Bootstrap': (re.compile(r'bootstrap([.-][\d\.]+)?(\.min)?\.(js|css)', re.I), None),
            'WordPress': (re.compile(r'/wp-content/|/wp-includes/|/wp-json/|wp-emoji-release\.min\.js', re.I), re.compile(r'x-powered-by:.*?WordPress|x-generator:.*?WordPress', re.I)),
            'Drupal': (re.compile(r'/sites/default/files/|misc/drupal\.js|core/assets/vendor',re.I), re.compile(r'x-generator:.*?Drupal', re.I)),
            'Joomla': (re.compile(r'/media/com_joomlaupdate/|/media/jui/',re.I), re.compile(r'x-content-encoded-by:.*?Joomla|x-generator:.*?Joomla', re.I)),
        }
        detected_tech_names = set()

        if response:
            for header_name, header_value in response.headers.items():
                full_header = f"{header_name.lower()}: {header_value.lower()}"
                for tech_name, (_, header_pattern) in tech_patterns.items():
                    if header_pattern and header_pattern.search(full_header):
                        detected_tech_names.add(tech_name)
        
        html_content_str = str(soup).lower() 
        scripts_srcs = " ".join([s.get('src','') for s in soup.find_all('script', src=True) if s.get('src')]).lower() # ensure src is not None
        meta_generators = " ".join([m.get('content','') for m in soup.find_all('meta', attrs={'name': 'generator'}) if m.get('content')]).lower() # ensure content is not None


        for tech_name, (content_pattern, _) in tech_patterns.items():
            if content_pattern:
                if content_pattern.search(html_content_str): 
                    detected_tech_names.add(tech_name)
                elif scripts_srcs and content_pattern.search(scripts_srcs): 
                    detected_tech_names.add(tech_name)
                elif meta_generators and content_pattern.search(meta_generators): 
                     detected_tech_names.add(tech_name)

        newly_detected_technologies = []
        existing_tech_names_in_session = {tech.nom_techno for tech in self.technologies}
        for tech_name in detected_tech_names:
            if tech_name not in existing_tech_names_in_session:
                version = "" 
                if response and tech_name == 'PHP' and 'x-powered-by' in response.headers:
                    match = re.search(r'PHP/([\d\.]+)', response.headers['x-powered-by'], re.I)
                    if match: version = match.group(1)
                elif tech_name == 'WordPress' and meta_generators:
                     match = re.search(r'wordpress\s*([\d\.]+)', meta_generators, re.I)
                     if match: version = match.group(1)
                
                tech_obj = Technologie(nom_techno=tech_name, version_techno=version)
                newly_detected_technologies.append(tech_obj)
                self.technologies.append(tech_obj) 
        
        return newly_detected_technologies


    def crawl(self, db: Session):
        logger.info(f"Crawler: Starting crawl for domain ID {self.domaine_model.id_domaine} ({self.base_url_str})")
        
        self.fuzzer.initialize_scan_session(db, self.domaine_model, self.base_url_str, self.max_depth)
        try:
            self.wordlist_content = self.fuzzer.load_wordlist(self.wordlist_name)
            logger.info(f"Crawler: Wordlist '{self.wordlist_name}' loaded successfully via fuzzer.")
        except FileNotFoundError:
            logger.error(f"Crawler: Wordlist '{self.wordlist_name}' not found. Fuzzing will be skipped.")
            self.wordlist_content = [] 

        initial_normalized_url = self.normalize_url(self.base_url_str)
        queue = deque([(initial_normalized_url, 0, None)])
        self.queued_urls_crawler.add(initial_normalized_url)

        while queue:
            current_url_str, depth, parent_sd_id = queue.popleft()
            # URL is already normalized from when it was added to queue.

            if not self.should_crawl_url(current_url_str, depth): 
                 # Exception: if already visited but at a greater depth, we might re-process
                 is_revisit_shallower = (current_url_str in self.visited_urls_crawler and
                                        current_url_str in self.sous_domaines_crawler_map and
                                        self.sous_domaines_crawler_map[current_url_str].degre > depth)
                 if not is_revisit_shallower:
                    logger.debug(f"Crawler: Skipping {current_url_str} (depth {depth}) due to should_crawl_url or already processed optimally.")
                    continue
                 else: # Re-processing at a shallower depth
                     logger.info(f"Crawler: Re-visiting {current_url_str} at shallower depth {depth} (prev_depth: {self.sous_domaines_crawler_map[current_url_str].degre}).")
            
            self.visited_urls_crawler.add(current_url_str) # Mark as visited (or re-visited)
            # Remove from queued set as it's now being processed
            if current_url_str in self.queued_urls_crawler:
                self.queued_urls_crawler.remove(current_url_str)

            logger.info(f"Crawler: Visiting: {current_url_str} (Depth: {depth})")

            try:
                final_url_str, response = self.fuzzer.fetch_url(current_url_str)
                
                if final_url_str != current_url_str: 
                    logger.info(f"Crawler: URL {current_url_str} redirected to {final_url_str}")
                    normalized_redirected_url = self.normalize_url(final_url_str) 

                    if not self.should_crawl_url(normalized_redirected_url, depth): 
                        logger.debug(f"Crawler: Redirected URL {normalized_redirected_url} skipped after check.")
                        # If original URL was in queue, it's now processed (as a redirect), so commit any SD for it if needed
                        # Or just continue and don't create an SD for the original if it only redirects.
                        # For simplicity, we continue and the original URL won't get an SD unless it was processed before redirecting.
                        db.commit() # Commit any pending changes from before this URL.
                        continue
                    
                    current_url_str = normalized_redirected_url # Process the final URL
                    
                    # If this new current_url_str was already visited/queued, handle carefully
                    if current_url_str in self.visited_urls_crawler:
                        if current_url_str in self.sous_domaines_crawler_map and \
                           self.sous_domaines_crawler_map[current_url_str].degre <= depth:
                            logger.debug(f"Crawler: Redirected URL {current_url_str} was already visited optimally. Skipping.")
                            db.commit()
                            continue
                        else: # Found via redirect at a potentially better depth
                            logger.info(f"Crawler: Redirected URL {current_url_str} will be processed (possibly updating depth).")
                    
                    self.visited_urls_crawler.add(current_url_str) # Mark redirected as visited
                    if current_url_str in self.queued_urls_crawler:
                         self.queued_urls_crawler.remove(current_url_str)


                if not response or response.status_code != 200:
                    logger.warning(f"Crawler: Failed to fetch {current_url_str} or non-200 status: {response.status_code if response else 'No response'}")
                    db.commit()
                    continue
                
                if 'text/html' not in response.headers.get('Content-Type', '').lower():
                    logger.debug(f"Crawler: Skipped non-HTML content at {current_url_str}")
                    db.commit()
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                current_sd_obj = self.fuzzer._get_or_create_sous_domaine(
                    db, current_url_str, f"Crawled at depth {depth}", depth, parent_sd_id
                )
                if not current_sd_obj: 
                    logger.error(f"Crawler: Failed to create/get SousDomaine for {current_url_str}")
                    db.commit()
                    continue
                
                self.sous_domaines_crawler_map[current_url_str] = current_sd_obj

                new_technos = self.extract_technologies(soup, response)
                for tech in new_technos:
                    # Check if already exists in DB to prevent duplicate primary key errors if not handled by model
                    existing_tech = db.query(Technologie).filter_by(nom_techno=tech.nom_techno, version_techno=tech.version_techno).first()
                    if not existing_tech:
                        db.add(tech) 
                if new_technos: 
                    db.flush() 
                    logger.info(f"Crawler: Processed {len(new_technos)} new/updated technologies from {current_url_str}")

                links_from_page = self.extract_links(soup, current_url_str) 
                for link in links_from_page:
                    if self.should_crawl_url(link, depth + 1): 
                        if link not in self.queued_urls_crawler : # Double check not already in queue by another path
                            queue.append((link, depth + 1, current_sd_obj.id_SD)) 
                            self.queued_urls_crawler.add(link) 

                if self.wordlist_content and current_sd_obj: 
                    logger.info(f"Crawler: Initiating fuzzing on SD: {current_sd_obj.url_SD} (ID: {current_sd_obj.id_SD}, Depth: {current_sd_obj.degre})")
                    
                    fuzzed_sds_created, fuzzed_pages_with_links = self.fuzzer.fuzz_single_url_paths(
                        db, 
                        current_sd_obj, 
                        self.wordlist_content
                    )
                    
                    for fuzzed_sd_obj, links_on_fuzzed_page in fuzzed_pages_with_links:
                        # fuzzed_sd_obj.degre is already depth of current_sd_obj + 1
                        if self.should_crawl_url(fuzzed_sd_obj.url_SD, fuzzed_sd_obj.degre): 
                            # The fuzzed page itself might need to be added to visited_urls_crawler
                            # and its SD object to sous_domaines_crawler_map if not already handled by fuzzer's map
                            if fuzzed_sd_obj.url_SD not in self.visited_urls_crawler:
                                self.visited_urls_crawler.add(fuzzed_sd_obj.url_SD) # Mark fuzzed page as visited by crawler too
                            if fuzzed_sd_obj.url_SD not in self.sous_domaines_crawler_map:
                                self.sous_domaines_crawler_map[fuzzed_sd_obj.url_SD] = fuzzed_sd_obj

                            for link_from_fuzzed in links_on_fuzzed_page: 
                                if self.should_crawl_url(link_from_fuzzed, fuzzed_sd_obj.degre + 1):
                                    if link_from_fuzzed not in self.queued_urls_crawler:
                                        logger.debug(f"Crawler: Adding link from fuzzed page {fuzzed_sd_obj.url_SD} to queue: {link_from_fuzzed}")
                                        queue.append((link_from_fuzzed, fuzzed_sd_obj.degre + 1, fuzzed_sd_obj.id_SD))
                                        self.queued_urls_crawler.add(link_from_fuzzed)
                db.commit()

            except requests.RequestException as e:
                logger.error(f"Crawler: Request error for {current_url_str}: {e}")
                db.rollback() 
            except Exception as e:
                logger.error(f"Crawler: Unexpected error processing {current_url_str}: {e}", exc_info=True)
                db.rollback()
        
        logger.info(f"Crawler: Crawl finished for {self.base_url_str}. Visited {len(self.visited_urls_crawler)} URLs.")
        logger.info(f"Crawler: Total SousDomaines in crawler map: {len(self.sous_domaines_crawler_map)}")
        logger.info(f"Crawler: Total Technologies found: {len(self.technologies)}")
        # Final commit (though we commit in loop now)
        # db.commit()


if __name__ == '__main__':
    from minattack.backend.app.database import SessionLocal, engine, Base as DBBase 
    from minattack.backend.app.models.user import User # Ensure User is imported for create_all context
    # Import all models by importing the models package, which should execute models/__init__.py
    import minattack.backend.app.models 

    logger.info("Cartographie_script __main__ block: Setting up for test run.")
    
    try:
        # Importing minattack.backend.app.models should have made all models known
        DBBase.metadata.create_all(bind=engine)
        logger.info("Cartographie_script __main__: Database tables checked/created.")
    except Exception as e:
        logger.error(f"Cartographie_script __main__: Error creating tables: {e}", exc_info=True)
        sys.exit(1)

    db: Session = SessionLocal()

    TARGET_URL = "http://testphp.vulnweb.com/" 
    WORDLIST_FILENAME = "test.csv" # Assumed in .../app/services/fuzzing/

    domaine = db.query(Domaine).filter(Domaine.url_domaine == TARGET_URL.rstrip('/')).first()
    if not domaine:
        domaine = Domaine(url_domaine=TARGET_URL.rstrip('/'), description_domaine="Test target from cartographie_script main")
        db.add(domaine)
        db.commit() 
        logger.info(f"Cartographie_script __main__: Created Domaine ID {domaine.id_domaine} for {domaine.url_domaine}")
    else:
        logger.info(f"Cartographie_script __main__: Using existing Domaine ID {domaine.id_domaine} for {domaine.url_domaine}")

    crawler = WebCrawler(
        base_url_str=TARGET_URL,
        domaine_obj=domaine,
        max_depth=1, 
        wordlist_name=WORDLIST_FILENAME, 
        verbose_fuzzer=True 
    )
    if crawler.fuzzer.verbose: 
        logger.setLevel(logging.DEBUG)

    try:
        crawler.crawl(db)
    except Exception as e:
        logger.error(f"Cartographie_script __main__: Error during crawl: {e}", exc_info=True)
        db.rollback()
    finally:
        if db.is_active:
            try:
                sds_after_crawl = db.query(SousDomaine).filter(SousDomaine.id_domaine  == domaine.id_domaine).all()
                logger.info(f"Found {len(sds_after_crawl)} SousDomaines for Domaine ID {domaine.id_domaine} after crawl:")
                for sd_item in sds_after_crawl:
                    logger.info(f"  SD ID: {sd_item.id_SD}, URL: {sd_item.url_SD}, Depth: {sd_item.degre}, Parent_SD_ID: {sd_item.id_SD_Sous_domaine}")

                attaques_after_crawl = db.query(minattack.backend.app.models.attaque.Attaque).join(SousDomaine).filter(SousDomaine.id_domaine  == domaine.id_domaine).all()
                logger.info(f"Found {len(attaques_after_crawl)} Attaques for Domaine ID {domaine.id_domaine}:")
            except Exception as e_query:
                 logger.error(f"Error querying results: {e_query}")
        
        db.close()
        logger.info("Cartographie_script __main__: Database session closed.")