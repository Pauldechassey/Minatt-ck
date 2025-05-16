INSERT INTO Domaine(url_domaine, description_domaine)VALUES
('http://127.0.0.1:5000', 'Domaine');

INSERT INTO Audit (date, etat, path_rapport, id_user, id_domaine) VALUES
('2023-10-01 12:00:00', 1, 'rapport.pdf', 1, 1);

INSERT INTO Sous_domaine (url_SD, description_SD, degre, id_domaine, id_SD_Sous_domaine) VALUES
('http://127.0.0.1:5000', 'Domaine', 1, 1, 1),
('http://127.0.0.1:5000/login', 'login', 2, 1, 1),
('http://127.0.0.1:5000/inscription', 'inscription', 2, 1, 1),
('http://127.0.0.1:5000/recherche', 'recherche', 2, 1, 1),
('http://127.0.0.1:5000/echo', 'echo', 2, 1, 1),
('http://127.0.0.1:5000/comments', 'comments', 2, 1, 1);

