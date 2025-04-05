PRAGMA foreign_keys = ON;

CREATE TABLE User (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_user TEXT NOT NULL,
    mdp_user TEXT NOT NULL,
    role INTEGER NOT NULL
);

CREATE TABLE Domaine (
    id_domaine INTEGER PRIMARY KEY AUTOINCREMENT,
    url_domaine TEXT NOT NULL,
    description_domaine TEXT
);

CREATE TABLE Audit (
    id_audit INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME NOT NULL,
    etat INTEGER NOT NULL,
    path_rapport TEXT,
    id_user INTEGER NOT NULL,
    id_domaine INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES User (id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_domaine) REFERENCES Domaine (id_domaine) ON DELETE CASCADE
);

CREATE TABLE Technologie (
    id_techno INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_techno TEXT NOT NULL,
    version_techno TEXT NOT NULL
);

CREATE TABLE Type_attaque (
    id_Type INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_type TEXT NOT NULL,
    description_type TEXT NOT NULL
);

CREATE TABLE Utiliser (
    id_domaine INTEGER NOT NULL,
    id_techno INTEGER NOT NULL,
    PRIMARY KEY (id_domaine, id_techno),
    FOREIGN KEY (id_domaine) REFERENCES Domaine (id_domaine) ON DELETE CASCADE,
    FOREIGN KEY (id_techno) REFERENCES Technologie (id_techno) ON DELETE CASCADE
);

CREATE TABLE Sous_domaine (
    id_SD INTEGER PRIMARY KEY AUTOINCREMENT,
    url_SD TEXT NOT NULL,
    description_SD TEXT NOT NULL,
    degre INTEGER NOT NULL,
    id_domaine INTEGER NOT NULL,
    id_SD_Sous_domaine INTEGER,
    FOREIGN KEY (id_SD_Sous_domaine) REFERENCES Sous_domaine (id_SD) ON DELETE CASCADE,
    FOREIGN KEY (id_domaine) REFERENCES Domaine (id_domaine) ON DELETE CASCADE
);

CREATE TABLE Attaque (
    id_attaque INTEGER PRIMARY KEY AUTOINCREMENT,
    payload TEXT NOT NULL,
    date_attaque DATETIME NOT NULL,
    resultat INTEGER NOT NULL,
    id_SD INTEGER NOT NULL,
    id_Type INTEGER NOT NULL,
    FOREIGN KEY (id_SD) REFERENCES Sous_domaine (id_SD) ON DELETE CASCADE,
    FOREIGN KEY (id_Type) REFERENCES Type_attaque (id_Type) ON DELETE CASCADE
);

CREATE TABLE Faille (
    id_faille INTEGER PRIMARY KEY AUTOINCREMENT,
    gravite INTEGER NOT NULL,
    Description TEXT NOT NULL,
    balise TEXT NOT NULL,
    id_attaque INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (id_attaque) REFERENCES Attaque (id_attaque) ON DELETE CASCADE
);

INSERT INTO User (nom_user, mdp_user, role) VALUES
('admin', '1eb1afa20dc454d6ef3b6dc6abcbd7dca7e519b698fdf073f4625ded09d74807', 1);

INSERT INTO Domaine(url_domaine, description_domaine)VALUES
('http://127.0.0.1:5000', 'Domaine');

INSERT INTO Type_attaque (nom_type, description_type) VALUES
('sqli', 'Attaque visant à insérer des requêtes SQL malveillantes dans un champ d’entrée pour manipuler la base de données.'),
('xss', 'Attaque permettant d’injecter du code JavaScript malveillant dans une page web vue par un autre utilisateur.'),
('csrf', 'Attaque où un utilisateur est forcé d’exécuter des actions non désirées sur un autre site web où il est authentifié.'),
('headers_cookies', 'Exploitation des en-têtes HTTP ou des cookies pour voler des informations sensibles ou contourner des mécanismes de sécurité.');

INSERT INTO Sous_domaine (url_SD, description_SD, degre, id_domaine, id_SD_Sous_domaine) VALUES
('http://127.0.0.1:5000', 'Domaine', 1, 1, 1),
('http://127.0.0.1:5000/login', 'login', 2, 1, 1),
('http://127.0.0.1:5000/inscription', 'inscription', 2, 1, 1),
('http://127.0.0.1:5000/recherche', 'recherche', 2, 1, 1),
('http://127.0.0.1:5000/echo', 'echo', 2, 1, 1),
('http://127.0.0.1:5000/comments', 'comments', 2, 1, 1);

