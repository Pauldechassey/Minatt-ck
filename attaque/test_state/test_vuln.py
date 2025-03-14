from flask import Flask, request, render_template_string, g, redirect, url_for, session
import sqlite3
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clé pour les sessions
user=""

# Connexion à la base SQLite (non sécurisée)
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db', check_same_thread=False)
        # Création des tables si elles n'existent pas
        g.db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
        g.db.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, username TEXT, comment TEXT, date TEXT)")
        g.db.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, ip TEXT, action TEXT, date TEXT)")
        g.db.execute("CREATE TABLE IF NOT EXISTS secrets (id INTEGER PRIMARY KEY, content TEXT)")
        
        # Insertion de données par défaut si la base est vide
        if g.db.execute("SELECT * FROM users").fetchone() is None:
            g.db.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'password123', 'admin'), ('test', '1234', 'user')")
            g.db.execute("INSERT INTO comments (username, comment, date) VALUES ('admin', 'Bienvenue sur notre site !', '2025-03-13')")
            g.db.execute("INSERT INTO logs (ip, action, date) VALUES ('127.0.0.1', 'Initialisation système', '2025-03-13')")
            g.db.execute("INSERT INTO logs (ip, action, date) VALUES ('192.168.1.1', 'Tentative de connexion réussie', '2025-03-13')")
            g.db.execute("INSERT INTO logs (ip, action, date) VALUES ('10.0.0.5', 'Mise à jour de la base de données', '2025-03-13')")
            g.db.execute("INSERT INTO logs (ip, action, date) VALUES ('172.16.0.1', 'Tentative de connexion échouée', '2025-03-13')")
            g.db.execute("INSERT INTO secrets (content) VALUES ('MDP_BDD_PROD=SuperSecret123!'), ('API_KEY=a1b2c3d4e5f6g7h8i9j0')")
            g.db.commit()
    return g.db


@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Fonction pour enregistrer une action dans les logs
def log_action(action, ip=None):
    if not ip:
        ip = request.remote_addr
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db.execute("INSERT INTO logs (ip, action, date) VALUES (?, ?, ?)", (ip, action, date))
    db.commit()

def get_current_user():
    if 'username' in session:
        return session['username']
    return None

@app.route('/')
def home():
    current_user = get_current_user()
    username_display = current_user if current_user else "💀 nobody_💀"
    db = get_db()
    comments_html = ""
    all_comments = db.execute("SELECT username, comment, date FROM comments ORDER BY id DESC").fetchall()
    
    for comment in all_comments:
        comments_html += f'''
        <div class="card mb-3">
            <div class="card-header">
                <strong>{comment[0]}</strong> - <small>{comment[2]}</small>
            </div>
            <div class="card-body">
                {comment[1]}
            </div>
        </div>
        '''
    
    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin-top: 50px;
                }
                h1 {
                    font-size: 2.5rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }
                p {
                    font-size: 0.9rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }                  
                .list-group-item {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                    margin-bottom: 15px; /* Espacement entre les boutons */
                    padding: 20px; /* Boutons remplis */
                }
                .list-group-item a {
                    color: #00ff00;
                    text-decoration: none; /* Supprime le soulignement */
                }
                .btn {
                    background-color: #00ff00;
                    color: #121212;
                    border: 1px solid #00ff00;
                }
                .btn:hover {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
                .card {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    margin-bottom: 15px;
                }
                .card-header {
                    background-color: #2a2a2a;
                    border-bottom: 1px solid #00ff00;
                    color: #00ff00;
                }
                .card-body {
                    color: #00ff00;
                }
                .user-info {
                    position: absolute;
                    top: 10px; /* Positionnement en haut */
                    right: 20px; /* Positionnement à droite */
                }
            </style>
            <title>Le Meilleur Site</title>
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">🔥 Le Meilleur Site 🔥</h1>
                <p></p>                  
                <p class="text-center">Le forum le plus sûr et le plus mieux du monde !</p>
                <p></p>
                <!-- Texte cliquable pour l'utilisateur -->
                <div class="user-info">
                    <a href="/profile" style="color:#00ff00; text-decoration:none;">i am : {{ username_display }}</a>
                </div>
                
                <!-- Contenu principal -->
                <div class="row">
                    
                    <!-- Colonne des commentaires -->
                    <div class="col-md-6">
                        <div class="comments">
                            {{ comments_html|safe }}
                        </div>
                    </div>
                    
                    <!-- Colonne des boutons -->
                    <div class="col-md-6 d-flex flex-column justify-content-start">
                        <ul class="list-group mt-0">
                            <li class="list-group-item"><a href="/login">Login/Inscription</a></li>
                            <li class="list-group-item"><a href="/recherche">Recherche</a></li>
                            <li class="list-group-item"><a href="/echo">Echo ton message</a></li>
                            <li class="list-group-item"><a href="/comments">Commentaires</a></li>
                            <li class="list-group-item"><a href="/profile">Profil Utilisateur</a></li>
                        </ul>
                    </div>
                    
                </div>
            </div>
        </body>
        </html>
    ''', comments_html=comments_html, username_display=username_display)


# Formulaire de connexion/inscription (SQLi vulnérable)
@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user = get_current_user()
    msg = ""
    if request.method == 'POST':
        action = request.form.get('action', '')
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        db = get_db()
        
        if action == 'login':
            # 🚨 Requête SQL VULNÉRABLE 🚨
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            res = db.execute(query).fetchall()

            if res:
                user=username
                session['username'] = username
                session['user_id'] = res[0][0]
                session['role'] = res[0][3]
                msg = f"✅ Connexion réussie ! Bienvenue {username}."
                log_action(f"Connexion de l'utilisateur {username}")
            else:
                msg = "❌ Accès refusé !"
                log_action(f"Tentative de connexion échouée pour {username}")
        
        elif action == 'register':
            # 🚨 Vulnérable à l'injection SQL dans la création de compte
            check_query = f"SELECT * FROM users WHERE username = '{username}'"
            existing = db.execute(check_query).fetchone()
            
            if existing:
                msg = "❌ Nom d'utilisateur déjà utilisé !"
            else:
                # Note: vulnérable car utilise des paramètres directs sans échappement
                user=username
                insert_query = f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', 'user')"
                db.execute(insert_query)
                db.commit()
                msg = f"✅ Compte créé avec succès ! Bienvenue {username}."
                log_action(f"Création du compte utilisateur {username}")

    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin-top: 50px;
                }
                h1 {
                    font-size: 2.5rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }
                .form-group {
                    margin-bottom: 1.5rem;
                }
                .form-control {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                }
                .btn {
                    background-color: #00ff00;
                    color: #121212;
                    border: 1px solid #00ff00;
                }
                .btn:hover {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
                .nav-tabs {
                    border-bottom: 1px solid #00ff00;
                }
                .nav-tabs .nav-link {
                    color: #00ff00;
                }
                .nav-tabs .nav-link.active {
                    background-color: #1e1e1e;
                    color: #00ff00;
                    border-color: #00ff00;
                }
            </style>
            <title>Login/Inscription</title>
        </head>
        <body>
            <div class="container text-center">
                <h1>💀 Login/Inscription 💀</h1>
                {% if current_user %}
                    <p>i am : {{ current_user }}</p>
                {% endif %}                   
                
                <ul class="nav nav-tabs" id="authTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="login-tab" data-toggle="tab" href="#login" role="tab" aria-controls="login" aria-selected="true">Connexion</a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="register-tab" data-toggle="tab" href="#register" role="tab" aria-controls="register" aria-selected="false">Inscription</a>
                    </li>
                </ul>
                
                <div class="tab-content mt-3" id="authTabsContent">
                    <div class="tab-pane fade show active" id="login" role="tabpanel" aria-labelledby="login-tab">
                        <form method="post">
                            <input type="hidden" name="action" value="login">
                            <div class="form-group">
                                <label for="username">Nom d'utilisateur</label>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                            <div class="form-group">
                                <label for="password">Mot de passe</label>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                            <button type="submit" class="btn">Se connecter</button>
                        </form>
                    </div>
                    
                    <div class="tab-pane fade" id="register" role="tabpanel" aria-labelledby="register-tab">
                        <form method="post">
                            <input type="hidden" name="action" value="register">
                            <div class="form-group">
                                <label for="reg_username">Nom d'utilisateur</label>
                                <input type="text" class="form-control" id="reg_username" name="username" required>
                            </div>
                            <div class="form-group">
                                <label for="reg_password">Mot de passe</label>
                                <input type="password" class="form-control" id="reg_password" name="password" required>
                            </div>
                            <button type="submit" class="btn">S'inscrire</button>
                        </form>
                    </div>
                </div>
                
                <p class="mt-3">{{ msg }}</p>
                <a href="/" class="btn mt-3">Retour</a>
            </div>
            
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
    ''', msg=msg, current_user=current_user)

# Recherche d'utilisateur vulnérable à SQLi
@app.route('/recherche')
def sqli():
    current_user = get_current_user()
    query = request.args.get('query', '')
    result = ""

    if query:
        db = get_db()
        sql = f"SELECT username FROM users WHERE username LIKE '%{query}%'"
        res = db.execute(sql).fetchall()

        result = "<br>".join(user[0] for user in res) if res else "Aucun résultat trouvé."

    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin-top: 50px;
                }
                h1 {
                    font-size: 2.5rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }
                .form-group {
                    margin-bottom: 1.5rem;
                }
                .form-control {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                }
                .btn {
                    background-color: #00ff00;
                    color: #121212;
                    border: 1px solid #00ff00;
                }
                .btn:hover {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
            </style>
            <title>Recherche SQLi</title>
        </head>
        <body>
            <div class="container text-center">
                <h1>🔍 Recherche 🔍</h1>
                {% if current_user %}
                    <p>i am : {{ current_user }}</p>
                {% endif %}
                <form method="get">
                    <div class="form-group">
                        <label for="query">Rechercher un utilisateur</label>
                        <input type="text" class="form-control" id="query" name="query" required>
                    </div>
                    <button type="submit" class="btn">Rechercher</button>
                </form>
                <p class="mt-3">Résultat : {{ result }}</p>
                <a href="/" class="btn mt-3">Retour</a>
            </div>
        </body>
        </html>
    ''', result=result, current_user=current_user)

# Page vulnérable au XSS
@app.route('/echo')
def echo():
    current_user = get_current_user()
    message = request.args.get('message', '')

    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin-top: 50px;
                }
                h1 {
                    font-size: 2.5rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }
                .form-group {
                    margin-bottom: 1.5rem;
                }
                .form-control {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                }
                .btn {
                    background-color: #00ff00;
                    color: #121212;
                    border: 1px solid #00ff00;
                }
                .btn:hover {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
            </style>
            <title>Test XSS</title>
        </head>
        <body>
            <div class="container text-center">
                <h1>💥 Echo ton message 💥</h1>
                {% if current_user %}
                    <p>i am : {{ current_user }}</p>
                {% endif %}                  
                <form method="get">
                    <div class="form-group">
                        <label for="message">Entrez un message</label>
                        <input type="text" class="form-control" id="message" name="message" required>
                    </div>
                    <button type="submit" class="btn">Envoyer</button>
                </form>
                <p class="mt-3">Message : ''' + message + '''</p>
                <a href="/" class="btn mt-3">Retour</a>
            </div>
        </body>
        </html>
    ''', current_user=current_user)


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    current_user = get_current_user()
    db = get_db()
    message = ""
    
    if request.method == 'POST':
        username = current_user if current_user else 'Anonyme'
        comment = request.form.get('comment', '')
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Stockage sans échappement (vulnérable au Stored XSS)
        db.execute(f"INSERT INTO comments (username, comment, date) VALUES ('{username}', '{comment}', '{date}')")
        db.commit()
        message = "✅ Commentaire ajouté avec succès !"
    
    # Récupération des commentaires
    all_comments = db.execute("SELECT username, comment, date FROM comments ORDER BY id DESC").fetchall()
    
    comments_html = ""
    for comment in all_comments:
        comments_html += f'''
        <div class="card mb-3">
            <div class="card-header">
                <strong>{comment[0]}</strong> - <small>{comment[2]}</small>
            </div>
            <div class="card-body">
                {comment[1]}
            </div>
        </div>
        '''
    
    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin-top: 50px;
                }
                h1 {
                    font-size: 2.5rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }
                .form-group {
                    margin-bottom: 1.5rem;
                }
                .form-control {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                }
                .btn {
                    background-color: #00ff00;
                    color: #121212;
                    border: 1px solid #00ff00;
                }
                .btn:hover {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
                .card {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    margin-bottom: 15px;
                }
                .card-header {
                    background-color: #2a2a2a;
                    border-bottom: 1px solid #00ff00;
                    color: #00ff00;
                }
                .card-body {
                    color: #00ff00;
                }
            </style>
            <title>Commentaires</title>
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">💬 Commentaires 💬</h1>
                {% if current_user %}
                    <p>i am : {{ current_user }}</p>
                {% endif %}                   
                <div class="row">
                    <div class="col-md-6 offset-md-3">
                        <form method="post" class="mb-4">
                            <div class="form-group">
                                <label for="comment">Commentaire</label>
                                <textarea class="form-control" id="comment" name="comment" rows="3" required></textarea>
                            </div>
                            <button type="submit" class="btn btn-block">Envoyer</button>
                        </form>
                        
                        <p class="text-center">{{ message }}</p>
                        
                        <div class="comments">
                            {{ comments_html|safe }}
                        </div>
                        
                        <div class="text-center mt-4">
                            <a href="/" class="btn">Retour</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''', message=message, comments_html=comments_html, current_user=current_user)


# Page profil utilisateur
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    db = get_db()
    user_id = session['user_id']
    user = db.execute(f"SELECT id, username, role FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if not user:
        return "Utilisateur non trouvé", 404
    
    return render_template_string('''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background-color: #121212;
                    color: #00ff00;
                    font-family: 'Courier New', Courier, monospace;
                }
                .container {
                    margin-top: 50px;
                }
                h1 {
                    font-size: 2.5rem;
                    text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
                }
                .card {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                }
                .card-header {
                    background-color: #2a2a2a;
                    border-bottom: 1px solid #00ff00;
                }
                .btn {
                    background-color: #00ff00;
                    color: #121212;
                    border: 1px solid #00ff00;
                }
                .btn:hover {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
                .list-group-item {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                }
            </style>
            <title>Profil Utilisateur</title>
        </head>
        <body>
            <div class="container">
                <h1 class="text-center">👤 Profil Utilisateur 👤</h1>
                {% if current_user %}
                    <p>i am : {{ current_user }}</p>
                {% endif %}
                <div class="row">
                    <div class="col-md-6 offset-md-3">
                        <div class="card">
                            <div class="card-header">
                                <h3>Informations utilisateur</h3>
                            </div>
                            <div class="card-body">
                                <ul class="list-group">
                                    <li class="list-group-item">ID: {{ user[0] }}</li>
                                    <li class="list-group-item">Nom d'utilisateur: {{ user[1] }}</li>
                                    <li class="list-group-item">Role: {{ user[2] }}</li>
                                </ul>
                            </div>
                        </div>
                        <div class="text-center mt-4">
                            <a href="/" class="btn">Retour</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
    ''', user=user, current_user=current_user)

    

if __name__ == '__main__':
    app.run(debug=True)