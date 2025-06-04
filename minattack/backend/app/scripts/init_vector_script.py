from typing import Any, Dict
import numpy as np
import re
from bs4 import BeautifulSoup


class InitVector:
    def __init__(self, web_content: str):
        self.web_content = web_content
        self.soup = BeautifulSoup(web_content, 'html.parser')
        self.vector_structure = self._build_vector_structure() 
        self.binary_vector = self._init_empty_vector(len(self.vector_structure))
        
        self._analyze_content()

    def _build_vector_structure(self) -> Dict[str, Dict[str, Any]]:
        """
        Construit la structure complète du vecteur
        Retourne un mapping {feature_name: {index: int, category: str, weight: float}}
        """
        structure = {}
        current_index = 0
        
        # === 1. EMPREINTE TECHNOLOGIQUE (25 dimensions) ===
        
        # CMS et frameworks (10)
        cms_frameworks = [
            "wordpress", "drupal", "joomla", "magento", "shopify", 
            "wix", "ghost", "prestashop", "typo3", "sharepoint"
        ]
        for cms in cms_frameworks:
            structure[f"cms_{cms}"] = {
                "index": current_index,
                "category": "cms_frameworks", 
                "weight": 2.0 if cms in ["wordpress", "drupal", "joomla", "magento"] else 1.0,
                "description": f"Site utilise {cms.capitalize()}"
            }
            current_index += 1
        
        # Frameworks web principaux (10)
        web_frameworks = [
            "php", "aspnet", "java", "nodejs", "rails", 
            "django", "laravel", "express", "react", "angular"
        ]
        for framework in web_frameworks:
            structure[f"framework_{framework}"] = {
                "index": current_index,
                "category": "web_frameworks",
                "weight": 1.0,
                "description": f"Site utilise {framework.upper()}"
            }
            current_index += 1
        
        # Architecture (5)
        architecture_features = [
            ("spa", "Single Page Application"),
            ("ssr", "Server-side Rendering"), 
            ("api_rest", "APIs REST publiques"),
            ("api_graphql", "APIs GraphQL publiques"),
            ("websockets", "WebSockets actifs")
        ]
        for feature, desc in architecture_features:
            structure[f"arch_{feature}"] = {
                "index": current_index,
                "category": "architecture",
                "weight": 1.5 if "api" in feature else 1.0,
                "description": desc
            }
            current_index += 1
        
        # === 2. PROFIL DE VULNÉRABILITÉ (40 dimensions) ===
        
        # Gestion d'authentification (10)
        auth_features = [
            ("login_traditional", "Login traditionnel (username/password)", 2.0),
            ("oauth", "OAuth implémenté", -0.5),
            ("jwt", "JWT utilisé", 1.0),
            ("session_cookies", "Session cookies", 1.0),
            ("saml_sso", "SAML/SSO implémentés", -0.5),
            ("has_2fa", "2FA disponible", -2.0),
            ("password_reset", "Réinitialisation de mot de passe", 2.0),
            ("user_registration", "Enregistrement d'utilisateurs", 1.5),
            ("role_access_control", "Contrôle d'accès par rôles", -0.5),
            ("auto_logout", "Auto-logout implémenté", -0.5)
        ]
        for feature, desc, weight in auth_features:
            structure[f"auth_{feature}"] = {
                "index": current_index,
                "category": "authentication",
                "weight": weight,
                "description": desc
            }
            current_index += 1
        
        # Traitement des entrées (15)
        input_features = [
            ("complex_forms", "Formulaires complexes (>5 champs)", 2.0),
            ("file_upload", "Upload de fichiers", 3.0),
            ("text_search", "Recherche texte intégral", 2.0),
            ("multiple_get_params", "Paramètres GET multiples", 1.5),
            ("url_state", "États persistés en URL", 1.5),
            ("json_input", "Entrées JSON acceptées", 2.0),
            ("xml_input", "Entrées XML acceptées", 2.0),
            ("api_keys_in_params", "API keys en paramètres", 3.0),
            ("rich_text_html", "Champs de texte riches/HTML", 3.0),
            ("external_iframes", "iFrames de tierces parties", 2.0),
            ("custom_redirects", "Redirections personnalisables", 3.0),
            ("data_import", "Importation de données", 2.5),
            ("data_export", "Exportation de données", 2.0),
            ("date_number_parsing", "Parsing de dates/nombres", 1.5),
            ("custom_session_mgmt", "Gestion de sessions personnalisée", 2.5)
        ]
        for feature, desc, weight in input_features:
            structure[f"input_{feature}"] = {
                "index": current_index,
                "category": "input_processing",
                "weight": weight,
                "description": desc
            }
            current_index += 1
        
        # Stockage et accès aux données (15)
        data_features = [
            ("sql_database", "Base de données SQL", 1.5),
            ("nosql_database", "NoSQL database", 1.0),
            ("file_access", "Accès à des fichiers", 2.0),
            ("client_cache", "Cache client (localStorage)", 1.0),
            ("external_api_calls", "API externes appelées côté serveur", 1.5),
            ("pii_visible", "Données sensibles visibles (PII)", 3.0),
            ("financial_data", "Information financière", 3.0),
            ("health_data", "Données de santé", 3.0),
            ("multi_step_workflow", "Workflow multi-étapes", 2.0),
            ("transactional_state", "États transactionnels", 2.0),
            ("cors_active", "Partage de ressources (CORS active)", 1.5),
            ("user_generated_content", "Contenus générés par utilisateurs", 2.5),
            ("comment_system", "Système de commentaires", 2.0),
            ("direct_file_download", "Téléchargement direct de fichiers", 2.0),
            ("internal_messaging", "Système de messagerie interne", 2.0)
        ]
        for feature, desc, weight in data_features:
            structure[f"data_{feature}"] = {
                "index": current_index,
                "category": "data_storage",
                "weight": weight,
                "description": desc
            }
            current_index += 1
        
        # === 3. INDICATEURS DE DÉFENSES (15 dimensions) ===
        
        defense_features = [
            ("waf_detected", "WAF détecté", -2.0),
            ("csp_strict", "CSP strict implémenté", -1.5),
            ("rate_limiting", "Rate limiting observé", -2.0),
            ("captcha", "CAPTCHA/reCAPTCHA", -1.0),
            ("sri", "SRI (Subresource Integrity)", -0.5),
            ("hsts", "HTTPS strict (HSTS)", -1.0),
            ("secure_cookies", "Cookies avec flags de sécurité", -1.0),
            ("csrf_tokens", "Anti-CSRF tokens", -2.0),
            ("server_validation", "Validation côté serveur forte", -1.5),
            ("security_headers", "En-têtes de sécurité complets", -1.0),
            ("secure_cdn", "Cloudflare ou autre CDN sécurisé", -1.0),
            ("ddos_protection", "Protection DDoS", -0.5),
            ("js_obfuscation", "Obfuscation JavaScript", -0.5),
            ("input_filtering", "Filtrage d'entrées visible", -1.0),
            ("honeypots", "Honeypots/détection de bots", -1.0)
        ]
        for feature, desc, weight in defense_features:
            structure[f"defense_{feature}"] = {
                "index": current_index,
                "category": "defenses",
                "weight": weight,
                "description": desc
            }
            current_index += 1
        
        # === 4. SPÉCIFICITÉS IMPACTANT LE TESTING (10 dimensions) ===
        
        testing_features = [
            ("api_quota", "APIs avec quota limité", 1.0),
            ("paywall", "Fonctionnalités paywall/premium", 1.0),
            ("mfa_required", "Authentification multi-facteurs requise", -1.0),
            ("geo_restriction", "Géo-restriction", 0.5),
            ("phone_validation", "Validation téléphonique requise", 0.5),
            ("async_states", "États asynchrones (polling/websockets)", 1.5),
            ("complex_workflow", "Workflow complexe avec état", 2.0),
            ("microservices", "Architecture microservices exposée", 1.5),
            ("dynamic_state", "Site dynamique à état (non-idempotent)", 1.5),
            ("client_cert_auth", "Authentification par certificat client", -0.5)
        ]
        for feature, desc, weight in testing_features:
            structure[f"testing_{feature}"] = {
                "index": current_index,
                "category": "testing_specifics",
                "weight": weight,
                "description": desc
            }
            current_index += 1
        
        return structure
    
    def _init_empty_vector(self, size) -> np.ndarray:
        """Crée un vecteur vide (tous les éléments à 0)"""
        return np.zeros(size)
    
    def _analyze_content(self):
        """Analyse le contenu web et remplit le vecteur binaire"""
        content_lower = self.web_content.lower()
        
        # === DÉTECTION CMS ===
        self._detect_cms(content_lower)
        
        # === DÉTECTION FRAMEWORKS ===
        self._detect_frameworks(content_lower)
        
        # === DÉTECTION ARCHITECTURE ===
        self._detect_architecture(content_lower)
        
        # === DÉTECTION AUTHENTIFICATION ===
        self._detect_authentication()
        
        # === DÉTECTION TRAITEMENT D'ENTRÉES ===
        self._detect_input_processing()
        
        # === DÉTECTION STOCKAGE DE DONNÉES ===
        self._detect_data_storage(content_lower)
        
        # === DÉTECTION DÉFENSES ===
        self._detect_defenses(content_lower)
        
        # === DÉTECTION SPÉCIFICITÉS TESTING ===
        self._detect_testing_specifics(content_lower)
    
    def _set_feature(self, feature_name: str, value: bool = True):
        """Active/désactive une feature dans le vecteur"""
        if feature_name in self.vector_structure:
            index = self.vector_structure[feature_name]["index"]
            self.binary_vector[index] = 1.0 if value else 0.0
    
    def _detect_cms(self, content_lower: str):
        """Détecte le CMS utilisé"""
        cms_patterns = {
            'wordpress': [r'wp-content', r'wp-includes', r'wordpress', r'wp-admin', r'/wp-json/'],
            'drupal': [r'drupal', r'sites/default', r'misc/drupal', r'\/core\/', r'drupal\.js'],
            'joomla': [r'joomla', r'administrator/index\.php', r'media/system/js', r'option=com_'],
            'magento': [r'magento', r'mage/cookies\.js', r'skin/frontend', r'var/view_preprocessed'],
            'shopify': [r'shopify', r'cdn\.shopify\.com', r'shopifycdn\.com'],
            'wix': [r'wix\.com', r'wixstatic\.com'],
            'ghost': [r'ghost', r'ghost\.org'],
            'prestashop': [r'prestashop', r'ps_faviconnotificationbo', r'modules/ps_'],
            'typo3': [r'typo3', r'typo3conf'],
            'sharepoint': [r'sharepoint', r'_layouts']
        }
        
        for cms, patterns in cms_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    self._set_feature(f'cms_{cms}')
                    break
    
    def _detect_frameworks(self, content_lower: str):
        """Détecte les frameworks utilisés"""
        framework_patterns = {
            'php': [r'\.php', r'phpsessid'],
            'aspnet': [r'\.aspx?', r'asp\.net', r'__viewstate'],
            'java': [r'jsessionid', r'\.jsp', r'\.do\?'],
            'nodejs': [r'node\.js', r'nodejs'],
            'rails': [r'rails', r'authenticity_token'],
            'django': [r'django', r'csrfmiddlewaretoken'],
            'laravel': [r'laravel', r'laravel_session'],
            'express': [r'express'],
            'react': [r'react', r'__reactinternalinstance'],
            'angular': [r'angular', r'ng-']
        }
        
        for framework, patterns in framework_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    self._set_feature(f'framework_{framework}')
                    break
    
    def _detect_architecture(self, content_lower: str):
        """Détecte l'architecture du site"""
        # SPA
        if re.search(r'single.?page.?application|spa', content_lower):
            self._set_feature('arch_spa')
        
        # API REST
        if re.search(r'/api/|rest|restful', content_lower):
            self._set_feature('arch_api_rest')
        
        # GraphQL
        if re.search(r'graphql|/graphql', content_lower):
            self._set_feature('arch_api_graphql')
        
        # WebSockets
        if re.search(r'websocket|socket\.io', content_lower):
            self._set_feature('arch_websockets')
    
    def _detect_authentication(self):
        """Détecte les mécanismes d'authentification"""
        # Login traditionnel
        login_forms = self.soup.find_all('form')
        for form in login_forms:
            inputs = form.find_all('input')
            if any(inp.get('type') == 'password' for inp in inputs):
                self._set_feature('auth_login_traditional')
                break
        
        # OAuth
        if re.search(r'oauth|google.*login|facebook.*login', self.web_content.lower()):
            self._set_feature('auth_oauth')
        
        # JWT
        if re.search(r'jwt|json.*web.*token', self.web_content.lower()):
            self._set_feature('auth_jwt')
        
        # Session cookies
        if re.search(r'session|cookie', self.web_content.lower()):
            self._set_feature('auth_session_cookies')
        
        # 2FA
        if re.search(r'2fa|two.*factor|totp|authenticator', self.web_content.lower()):
            self._set_feature('auth_has_2fa')
        
        # Password reset
        if re.search(r'forgot.*password|reset.*password|password.*recovery', self.web_content.lower()):
            self._set_feature('auth_password_reset')
        
        # User registration
        if re.search(r'register|sign.*up|create.*account', self.web_content.lower()):
            self._set_feature('auth_user_registration')
    
    def _detect_input_processing(self):
        """Détecte le traitement des entrées"""
        forms = self.soup.find_all('form')
        
        for form in forms:
            inputs = form.find_all(['input', 'textarea', 'select'])
            
            # Formulaires complexes
            if len(inputs) > 5:
                self._set_feature('input_complex_forms')
            
            # Upload de fichiers
            if any(inp.get('type') == 'file' for inp in inputs):
                self._set_feature('input_file_upload')
        
        # Recherche
        if self.soup.find('input', {'type': 'search'}) or \
           self.soup.find('input', {'name': re.compile(r'search|query', re.I)}):
            self._set_feature('input_text_search')
        
        # Rich text editor
        if self.soup.find(attrs={'class': re.compile(r'editor|wysiwyg|tinymce|ckeditor', re.I)}):
            self._set_feature('input_rich_text_html')
        
        # iFrames externes
        iframes = self.soup.find_all('iframe')
        for iframe in iframes:
            src = iframe.get('src', '')
            if src and 'http' in src:  # iframe externe
                self._set_feature('input_external_iframes')
                break
        
        # CSRF tokens
        csrf_found = self.soup.find('input', {'name': re.compile(r'csrf|token', re.I)}) or \
                    self.soup.find('meta', {'name': re.compile(r'csrf', re.I)})
        if csrf_found:
            self._set_feature('defense_csrf_tokens')
    
    def _detect_data_storage(self, content_lower: str):
        """Détecte le stockage et l'accès aux données"""
        # Données sensibles
        if re.search(r'email|phone|address|credit.*card|ssn', content_lower):
            self._set_feature('data_pii_visible')
        
        # Données financières
        if re.search(r'payment|billing|price|€|\$|bank|financial', content_lower):
            self._set_feature('data_financial_data')
        
        # Système de commentaires
        if self.soup.find(attrs={'class': re.compile(r'comment|review', re.I)}):
            self._set_feature('data_comment_system')
        
        # Contenu généré par utilisateurs
        if re.search(r'upload|post|comment|review|rating', content_lower):
            self._set_feature('data_user_generated_content')
        
        # Cache client
        if re.search(r'localstorage|sessionstorage|indexeddb', content_lower):
            self._set_feature('data_client_cache')
    
    def _detect_defenses(self, content_lower: str):
        """Détecte les mécanismes de défense"""
        # WAF (sera complété avec les headers HTTP)
        if re.search(r'cloudflare|incapsula|sucuri|aws.*waf', content_lower):
            self._set_feature('defense_waf_detected')
        
        # CAPTCHA
        if re.search(r'captcha|recaptcha|hcaptcha', content_lower):
            self._set_feature('defense_captcha')
        
        # CSP (nécessite les headers HTTP)
        if re.search(r'content.?security.?policy|csp', content_lower):
            self._set_feature('defense_csp_strict')
    
    def _detect_testing_specifics(self, content_lower: str):
        """Détecte les spécificités impactant le testing"""
        if re.search(r'premium|subscription|paywall|upgrade', content_lower):
            self._set_feature('testing_paywall')
        
        if re.search(r'step.*\d|wizard|multi.*step', content_lower):
            self._set_feature('testing_complex_workflow')
    
    def get_vector(self) -> np.ndarray:
        """Retourne le vecteur binaire"""
        return self.binary_vector
    
    def get_active_features(self) -> Dict[str, Any]:
        """Retourne les features actives avec leurs informations"""
        active_features = {}
        for feature_name, info in self.vector_structure.items():
            index = info["index"]
            if self.binary_vector[index] == 1.0:
                active_features[feature_name] = info
        return active_features
    
    def calculate_weighted_score(self) -> float:
        """Calcule le score pondéré du vecteur"""
        total_score = 0.0
        for feature_name, info in self.vector_structure.items():
            index = info["index"]
            weight = info["weight"]
            if self.binary_vector[index] == 1.0:
                total_score += weight
        return total_score
    
    def print_analysis(self):
        """Affiche l'analyse du site"""
        active_features = self.get_active_features()
        score = self.calculate_weighted_score()
        
        print(f"🔍 ANALYSE DU SITE WEB")
        print(f"=" * 50)
        print(f"📊 Features détectées: {len(active_features)}/{self.vector_size}")
        print(f"⚖️  Score pondéré: {score:.2f}")
        print(f"\n🎯 FEATURES ACTIVES:")
        
        for feature_name, info in active_features.items():
            weight = info["weight"]
            desc = info["description"]
            category = info["category"]
            sign = "+" if weight >= 0 else ""
            print(f"   [{category}] {feature_name}: {sign}{weight} - {desc}")

