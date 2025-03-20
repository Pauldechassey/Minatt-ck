import json
from datetime import datetime
from fpdf import FPDF
import textwrap
import os

class SecurityReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Rapport d\'analyse de sécurité', 0, 1, 'C')
        self.set_font('Helvetica', '', 12)
        self.cell(0, 10, f'Date: {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
        self.ln(10)
    
    def chapter_title(self, title, level=1):
        if level == 1:
            self.set_font('Helvetica', 'B', 14)
            self.set_fill_color(200, 220, 255)
            self.cell(0, 10, title, 0, 1, 'L', 1)
        elif level == 2:
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, title, 0, 1, 'L')
        else:
            self.set_font('Helvetica', 'BI', 12)
            self.cell(0, 8, title, 0, 1, 'L')
        self.ln(4)
    
    def body_text(self, text):
        self.set_font('Helvetica', '', 12)
        lines = textwrap.wrap(text, 80)
        for line in lines:
            self.cell(0, 6, line, 0, 1)
        self.ln(4)
    
    def bullet_point(self, text, level=1):
        self.set_font('Helvetica', '', 12)
        indent = level * 5
        bullet = '-' if level == 1 else '\-' if level == 2 else '\--'
        self.cell(indent)
        lines = textwrap.wrap(text, 80 - indent)
        if not lines:
            return
        self.cell(0, 6, f"{bullet} {lines[0]}", 0, 1)
        for line in lines[1:]:
            self.cell(indent + 5)
            self.cell(0, 6, line, 0, 1)
        self.ln(1)
    
    def add_vulnerability_table(self, vulns, title, headers, get_row_data):
        if not vulns:
            return False
        
        self.chapter_title(title)
        
        # Calculate column widths based on the available page width
        col_widths = [40, 50, 100]  # Adjusted for three columns
        
        # Table headers
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(220, 230, 240)
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', 1)
        self.ln()
        
        # Table data
        self.set_font('Helvetica', '', 10)
        for vuln in vulns:
            row_data = get_row_data(vuln)
            
            # Check if we need a new page for this row
            if self.get_y() + 10 > self.page_break_trigger:
                self.add_page()
                
                # Repeat headers on new page
                self.set_font('Helvetica', 'B', 10)
                self.set_fill_color(220, 230, 240)
                for i, header in enumerate(headers):
                    self.cell(col_widths[i], 8, header, 1, 0, 'C', 1)
                self.ln()
                self.set_font('Helvetica', '', 10)
            
            # Calculate the maximum height needed for this row
            max_height = 8
            wrapped_texts = []
            for j, text in enumerate(row_data):
                wrapped = textwrap.wrap(str(text), int(col_widths[j] / 2.5))
                wrapped_texts.append(wrapped)
                max_height = max(max_height, len(wrapped) * 6)
            
            # Start positions for each cell
            y_position = self.get_y()
            
            for j, wrapped in enumerate(wrapped_texts):
                self.set_xy(self.get_x() + (col_widths[j] if j > 0 else 0), y_position)
                
                # Draw cell border
                self.cell(col_widths[j], max_height, '', 1, 0)
                
                # Reset position to write text
                self.set_xy(self.get_x() - col_widths[j], y_position)
                
                # Write text
                for line in wrapped:
                    self.cell(col_widths[j], 6, line, 0, 2)
            
            # Move to next row
            self.set_xy(10, y_position + max_height)
        
        self.ln(10)
        return True
    
    def add_recommendations(self, section_title, recommendations):
        self.chapter_title(section_title)
        for rec_title, rec_details in recommendations.items():
            self.set_font('Helvetica', 'B', 12)
            self.cell(0, 8, rec_title, 0, 1, 'L')
            self.set_font('Helvetica', '', 12)
            self.multi_cell(0, 6, rec_details)
            self.ln(4)


def generate_security_report(scan_results, output_filename='rapport_securite.pdf'):
    """
    Génère un rapport PDF à partir des résultats d'analyse de sécurité.
    
    Args:
        scan_results (dict): Les résultats de scan de sécurité
        output_filename (str): Nom du fichier PDF de sortie
    """
    # Si les résultats sont une chaîne JSON, les convertir en dictionnaire
    if isinstance(scan_results, str):
        try:
            scan_results = json.loads(scan_results)
        except json.JSONDecodeError:
            raise ValueError("Les résultats fournis ne sont pas un JSON valide")
    
    pdf = SecurityReportPDF()
    
    # Résumé exécutif
    pdf.chapter_title("Résumé exécutif")
    
    # Compter les vulnérabilités par type
    vuln_counts = {
        "SQLi": sum(len(group) for group in scan_results.get('sqli', []) if group),
        "XSS": sum(len(group) for group in scan_results.get('xss', []) if group),
        "CSRF": sum(len(group) for group in scan_results.get('csrf', []) if group),
        "Headers": sum(len(group) for group in scan_results.get('headers_cookies', []) if group)
    }
    
    # Construire le résumé
    summary_text = f"""Cette analyse de sécurité a identifié plusieurs vulnérabilités critiques sur l'application web testée.
L'analyse a révélé {vuln_counts['SQLi']} vulnérabilités d'injection SQL, {vuln_counts['XSS']} vulnérabilités XSS, 
{vuln_counts['CSRF']} vulnérabilités CSRF et {vuln_counts['Headers']} problèmes liés aux en-têtes de sécurité.
Ces vulnérabilités représentent des risques importants pour la confidentialité, l'intégrité et la disponibilité des données.
Des mesures correctives doivent être prises immédiatement pour remédier à ces problèmes."""
    
    pdf.body_text(summary_text)
    pdf.ln(5)
    
    # Analyse des vulnérabilités SQL Injection
    pdf.chapter_title("1. Injections SQL (SQLi)")
    
    sqli_present = False
    for i, group in enumerate(scan_results.get('sqli', [])):
        if not group:
            continue
        
        sqli_present = True
        page_url = group[0]['url'] if group else "URL inconnue"
        pdf.chapter_title(f"Page: {page_url}", 2)
        
        for vuln in group:
            pdf.bullet_point(f"Champ vulnérable: {vuln['champ']}")
            pdf.bullet_point(f"Type: {vuln['type_vuln']}", 2)
            pdf.bullet_point(f"Payload testé: {vuln['payload']}", 2)
            pdf.bullet_point(f"Temps de réponse: {vuln['temps_reponse']} secondes", 2)
            if vuln['is_login_form']:
                pdf.bullet_point("Formulaire d'authentification: Oui", 2)
            pdf.ln(2)
    
    if not sqli_present:
        pdf.body_text("Aucune vulnérabilité d'injection SQL détectée.")
    
    # Analyse des vulnérabilités XSS
    pdf.chapter_title("2. Cross-Site Scripting (XSS)")
    
    xss_present = False
    for i, group in enumerate(scan_results.get('xss', [])):
        if not group:
            continue
        
        xss_present = True
        page_url = group[0]['url'] if group else "URL inconnue"
        pdf.chapter_title(f"Page: {page_url}", 2)
        
        for vuln in group:
            pdf.bullet_point(f"Type: {vuln['type']} XSS")
            pdf.bullet_point(f"Paramètre vulnérable: {vuln['param']}", 2)
            pdf.bullet_point(f"Payload testé: {vuln['payload']}", 2)
            if vuln['type'] == 'stored':
                pdf.bullet_point(f"URL d'affichage: {vuln.get('display_url', 'Non spécifié')}", 2)
            pdf.ln(2)
    
    if not xss_present:
        pdf.body_text("Aucune vulnérabilité XSS détectée.")
    
    # Analyse des vulnérabilités CSRF
    pdf.chapter_title("3. Cross-Site Request Forgery (CSRF)")
    
    csrf_present = False
    for i, group in enumerate(scan_results.get('csrf', [])):
        if not group:
            continue
        
        csrf_present = True
        
        for vuln in group:
            pdf.bullet_point(f"URL vulnérable: {vuln['url']}")
            pdf.bullet_point(f"Élément: {vuln['element']}", 2)
            pdf.bullet_point(f"Méthode: {vuln['method']}", 2)
            pdf.bullet_point(f"Preuve: {vuln['proof']}", 2)
            pdf.ln(2)
    
    if not csrf_present:
        pdf.body_text("Aucune vulnérabilité CSRF détectée.")
    
    # Analyse des problèmes d'en-têtes de sécurité
    pdf.chapter_title("4. Problèmes d'en-têtes de sécurité")
    
    # Créer un résumé des en-têtes manquants par URL
    headers_summary = {}
    
    for group in scan_results.get('headers_cookies', []):
        if not group:
            continue
        
        url = group[0]['url'] if group else "URL inconnue"
        missing_headers = [issue['element'].replace('Header: ', '') for issue in group]
        
        if url not in headers_summary:
            headers_summary[url] = set()
        
        headers_summary[url].update(missing_headers)
    
    if headers_summary:
        for url, headers in headers_summary.items():
            pdf.chapter_title(f"URL: {url}", 2)
            for header in sorted(headers):
                pdf.bullet_point(f"En-tête manquant: {header}")
            pdf.ln(2)
    else:
        pdf.body_text("Aucun problème d'en-têtes de sécurité détecté.")
    
    # Recommandations de correction
    pdf.add_page()
    pdf.chapter_title("Recommandations de sécurité")
    
    # Recommandations pour SQL Injection
    if sqli_present:
        pdf.chapter_title("Pour les injections SQL:", 2)
        pdf.bullet_point("Utiliser des requêtes paramétrées (prepared statements) avec des paramètres liés")
        pdf.bullet_point("Mettre en place un ORM (Object-Relational Mapping)")
        pdf.bullet_point("Valider les entrées utilisateur en utilisant une liste blanche")
        pdf.bullet_point("Limiter les privilèges de la base de données")
        pdf.bullet_point("Utiliser des procédures stockées")
        
        # Exemple de code pour corriger les injections SQL
        pdf.chapter_title("Exemple de correction en Python (Flask/SQLAlchemy):", 3)
        code_sqli = """
# Mauvaise pratique:
query = "SELECT * FROM users WHERE username = '" + username + "'"

# Bonne pratique avec SQLAlchemy:
user = db.session.query(User).filter(User.username == username).first()

# Bonne pratique avec requêtes paramétrées:
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
"""
        pdf.set_font('Courier', '', 10)
        for line in code_sqli.strip().split('\n'):
            pdf.cell(10)
            pdf.cell(0, 5, line, 0, 1)
        pdf.ln(5)
    
    # Recommandations pour XSS
    if xss_present:
        pdf.chapter_title("Pour les vulnérabilités XSS:", 2)
        pdf.bullet_point("Échapper les données de sortie en utilisant des bibliothèques d'échappement spécifiques au contexte")
        pdf.bullet_point("Mettre en place une politique de sécurité de contenu (CSP)")
        pdf.bullet_point("Utiliser des attributs HttpOnly et Secure pour les cookies")
        pdf.bullet_point("Valider les entrées utilisateur côté serveur")
        pdf.bullet_point("Utiliser des bibliothèques sécurisées pour le rendu HTML")
        
        # Exemple de code pour corriger les XSS
        pdf.chapter_title("Exemple de correction en Python (Flask):", 3)
        code_xss = """
# Mauvaise pratique:
@app.route('/echo')
def echo():
    message = request.args.get('message', '')
    return f"<p>{message}</p>"  # Vulnérable au XSS

# Bonne pratique:
from markupsafe import escape
@app.route('/echo')
def echo_secure():
    message = request.args.get('message', '')
    return f"<p>{escape(message)}</p>"  # Sécurisé
"""
        pdf.set_font('Courier', '', 10)
        for line in code_xss.strip().split('\n'):
            pdf.cell(10)
            pdf.cell(0, 5, line, 0, 1)
        pdf.ln(5)
    
    # Recommandations pour CSRF
    if csrf_present:
        pdf.chapter_title("Pour les vulnérabilités CSRF:", 2)
        pdf.bullet_point("Utiliser des jetons anti-CSRF dans les formulaires")
        pdf.bullet_point("Vérifier l'en-tête Referer pour les requêtes sensibles")
        pdf.bullet_point("Implémenter l'en-tête SameSite=Strict pour les cookies")
        pdf.bullet_point("Utiliser des mécanismes de double soumission de cookies")
        
        # Exemple de code pour corriger les CSRF
        pdf.chapter_title("Exemple de correction en Python (Flask):", 3)
        code_csrf = """
# Avec Flask-WTF:
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clé-secrète-difficile-à-deviner'
csrf = CSRFProtect(app)

# Dans le formulaire:
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Le jeton CSRF est automatiquement vérifié
        # Traitement du formulaire
        pass
    return render_template('profile.html', form=form)

# Dans le template HTML:
<form method="post">
    {{ form.csrf_token }}
    <!-- Autres champs du formulaire -->
    <button type="submit">Envoyer</button>
</form>
"""
        pdf.set_font('Courier', '', 10)
        for line in code_csrf.strip().split('\n'):
            pdf.cell(10)
            pdf.cell(0, 5, line, 0, 1)
        pdf.ln(5)
    
    # Recommandations pour les en-têtes de sécurité
    if headers_summary:
        pdf.chapter_title("Pour les problèmes d'en-têtes de sécurité:", 2)
        
        header_recs = {
            "Content-Security-Policy": "Définit les sources de contenu approuvées. Exemple: Content-Security-Policy: default-src 'self'",
            "X-Frame-Options": "Prévient le clickjacking. Exemple: X-Frame-Options: DENY",
            "X-Content-Type-Options": "Prévient le MIME-sniffing. Exemple: X-Content-Type-Options: nosniff",
            "X-XSS-Protection": "Active la protection XSS du navigateur. Exemple: X-XSS-Protection: 1; mode=block",
            "Strict-Transport-Security": "Force les connexions HTTPS. Exemple: Strict-Transport-Security: max-age=31536000; includeSubDomains",
            "Referrer-Policy": "Contrôle les informations du référent. Exemple: Referrer-Policy: no-referrer-when-downgrade"
        }
        
        # Exemple de code pour ajouter des en-têtes de sécurité
        pdf.chapter_title("Exemple d'ajout d'en-têtes de sécurité en Python (Flask):", 3)
        code_headers = """
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    return response
"""
        pdf.set_font('Courier', '', 10)
        for line in code_headers.strip().split('\n'):
            pdf.cell(10)
            pdf.cell(0, 5, line, 0, 1)
        pdf.ln(5)
        
        # Détail sur chaque en-tête
        for header, desc in header_recs.items():
            pdf.bullet_point(f"{header}: {desc}")
    
    # Conclusion
    pdf.add_page()
    pdf.chapter_title("Conclusion")
    
    conclusion_text = """
L'analyse de sécurité a révélé plusieurs vulnérabilités critiques qui nécessitent une attention immédiate. 
Ces problèmes exposent l'application web à des risques significatifs, notamment:

- Divulgation ou corruption de données sensibles via des injections SQL
- Vol de session et usurpation d'identité via des attaques XSS
- Exécution d'actions non autorisées via des attaques CSRF
- Exposition à diverses attaques dues à l'absence d'en-têtes de sécurité

Il est fortement recommandé de suivre les recommandations détaillées dans ce rapport et de mettre en place
un processus de développement sécurisé comprenant:

1. Formation de l'équipe de développement aux bonnes pratiques de sécurité
2. Tests de sécurité réguliers (SAST, DAST, tests de pénétration)
3. Revues de code axées sur la sécurité
4. Utilisation de bibliothèques et frameworks sécurisés et maintenus
5. Mise en place d'un programme de gestion des vulnérabilités

La sécurité est un processus continu qui nécessite une attention constante. Il est recommandé de procéder
à une nouvelle analyse après l'application des correctifs pour vérifier leur efficacité.
"""
    pdf.body_text(conclusion_text)
    
    # Sauvegarde du rapport
    pdf.output(output_filename)
    return output_filename
