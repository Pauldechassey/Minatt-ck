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