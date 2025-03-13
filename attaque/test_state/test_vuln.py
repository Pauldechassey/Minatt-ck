from flask import Flask, request, render_template_string, g
import sqlite3

app = Flask(__name__)

# Connexion à la base SQLite (non sécurisée)
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(":memory:", check_same_thread=False)
        g.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        g.db.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123'), ('test', '1234')")
        g.db.commit()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Page d'accueil
@app.route('/')
def home():
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
                .list-group-item {
                    background-color: #1e1e1e;
                    border: 1px solid #00ff00;
                    color: #00ff00;
                }
                .list-group-item a {
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
            <title>Site Vulnérable</title>
        </head>
        <body>
            <div class="container text-center">
                <h1>🔥 Site Vulnérable 🔥</h1>
                <ul class="list-group mt-3">
                    <li class="list-group-item"><a href="/login">Login (SQLi)</a></li>
                    <li class="list-group-item"><a href="/sqli">Recherche SQLi</a></li>
                    <li class="list-group-item"><a href="/xss">Test XSS</a></li>
                </ul>
            </div>
        </body>
        </html>
    ''')

# Formulaire de connexion (SQLi vulnérable)
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # 🚨 Requête SQL VULNÉRABLE 🚨
        db = get_db()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        res = db.execute(query).fetchall()

        if res:
            msg = f"✅ Connexion réussie ! Bienvenue {username}."
        else:
            msg = "❌ Accès refusé !"

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
            <title>Login</title>
        </head>
        <body>
            <div class="container text-center">
                <h1>💀 Login (SQLi) 💀</h1>
                <form method="post">
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
                <p class="mt-3">{{ msg }}</p>
                <a href="/" class="btn mt-3">Retour</a>
            </div>
        </body>
        </html>
    ''', msg=msg)

# Recherche d'utilisateur vulnérable à SQLi
@app.route('/sqli')
def sqli():
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
                <h1>🔍 Recherche SQLi 🔍</h1>
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
    ''', result=result)

# Page vulnérable au XSS
@app.route('/xss')
def xss():
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
                <h1>💥 Test XSS 💥</h1>
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
    ''')

if __name__ == '__main__':
    app.run(debug=True)
