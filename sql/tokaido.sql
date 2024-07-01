--
-- Création de la base de données :
--

DROP DATABASE IF EXISTS Tokaido;

CREATE DATABASE Tokaido CHARACTER SET 'utf8';

USE Tokaido;

--
-- Création des tables :
--

CREATE TABLE Joueur (
	jou_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	jou_nom VARCHAR(30) NOT NULL,
	jou_prenom VARCHAR(30) NOT NULL,
    jou_pseudo VARCHAR(20) NOT NULL,
	jou_creation DATE,
	jou_login VARCHAR(20) NOT NULL,
	jou_password VARCHAR(30) NOT NULL,
	PRIMARY KEY (jou_id)
)
ENGINE=INNODB;


CREATE TABLE Statistiques (
	sta_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	sta_win INT,
    sta_lose INT,
	PRIMARY KEY (sta_id),
    CONSTRAINT fk_sta_id FOREIGN KEY (sta_id) REFERENCES Joueur(jou_id)
)
ENGINE=INNODB;

--
-- Insertion de valeurs dans les tables :
--

INSERT INTO Joueur
VALUES	(1, 'CHEVREL', 'Arthur', 'Art333', '2023-03-15', 'rocknnarthur', 'raclette123!'),
(2, 'AMISI', 'Arthur', 'Vitarse', '2023-05-10', 'vitarse', 'azerty123*'),
(3, 'BENARD', 'Sam', 'Frimoosse', '2023-05-11', 'frimoosse', 'ratio123*'),
(4, 'LAGORCE', 'Simon', 'Zeldomar', '2023-05-13', 'zeldomar', 'flop123*'),
(5, 'CADORET', 'Clément', 'Rozdor', '2023-05-15', 'rozdor', '1234'),
(6, 'DUGUE', 'Alissa', 'Lauyana', '2023-05-16', 'lauyana', 'fromage123*');

INSERT INTO Statistiques
VALUES	(1, 0, 0),
(2, 0, 0),
(3, 0, 0),
(4, 0, 0),
(5, 0, 0),
(6, 0, 0);
