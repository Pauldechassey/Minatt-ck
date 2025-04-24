INSERT INTO User (nom_user, mdp_user, role) VALUES
('admin', '1eb1afa20dc454d6ef3b6dc6abcbd7dca7e519b698fdf073f4625ded09d74807', 1);

INSERT INTO Type_attaque (nom_type, description_type) VALUES
('sqli', 'Attaque visant à insérer des requêtes SQL malveillantes dans un champ d’entrée pour manipuler la base de données.'),
('xss', 'Attaque permettant d’injecter du code JavaScript malveillant dans une page web vue par un autre utilisateur.'),
('csrf', 'Attaque où un utilisateur est forcé d’exécuter des actions non désirées sur un autre site web où il est authentifié.'),
('headers_cookies', 'Exploitation des en-têtes HTTP ou des cookies pour voler des informations sensibles ou contourner des mécanismes de sécurité.');



