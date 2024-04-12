CREATE DATABASE agence_de_transport;
USE agence_de_transport;

CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur varchar(36) primary key,
    ut_username varchar(60),
    ut_password varchar(200),
    ut_nom varchar(20),
    ut_prenom varchar(20),
    ut_telephone varchar(10)
);

CREATE TABLE IF NOT EXISTS conducteur(
    id_conducteur varchar(36) PRIMARY KEY,
    username varchar(60),
    password varchar(200),
    nb_jour_conger INT DEFAULT 5
);


CREATE TABLE IF NOT EXISTS avis (
    vo_ni varchar(36),
    note enum('Excellent','Bien','Modeste','Mauvais','Aucune note'),
    commentaire varchar(200),
    id_utilisateur varchar(36),
    PRIMARY KEY (vo_ni, id_utilisateur),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur),
    FOREIGN KEY (vo_ni) REFERENCES voyage(vo_ni)
);

CREATE TABLE IF NOT EXISTS voyage (
    vo_ni varchar(36) primary key,
    vo_prix_passager integer,
    vo_heure_dep DATETIME not null,
    vo_dep varchar(255),
    vo_dest varchar(255),
    id_conducteur varchar(36),
    FOREIGN KEY (id_conducteur) REFERENCES conducteur(id_conducteur)
);



CREATE TABLE IF NOT EXISTS admins (
    id_admin varchar(36) primary key,
    adm_username varchar(20),
    adm_password varchar(200)
);

CREATE TABLE IF NOT EXISTS voyage_utilisateur(
    id_participation integer AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur varchar(36),
    vo_ni varchar(36),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur),
    FOREIGN KEY (vo_ni) REFERENCES voyage(vo_ni)
);

CREATE TABLE IF NOT EXISTS horaire_conducteur(
    id_conducteur varchar(36),
    date DATE,
    heure_debut TIME,
    heure_fin TIME,
    conger BOOL DEFAULT FALSE,
    voyage_av_midi BOOL DEFAULT FALSE,
    voyage_ap_midi BOOL DEFAULT FALSE,
    PRIMARY KEY (id_conducteur, date),
    FOREIGN KEY (id_conducteur) REFERENCES conducteur(id_conducteur)
);

CREATE TABLE IF NOT EXISTS serviceClient (
    sc_id integer primary key references employes (em_id),
    sc_nom varchar(20) references employes (em_nom),
    sc_prenom varchar(20) references employes (em_prenom),
    sc_th FLOAT references employes (em_th),
    sc_langue enum('ENG', 'FR', 'ESP', 'ARB', 'JPN', 'MAN')
); */

CREATE TABLE IF NOT EXISTS villes_quebec (
    id_ville INT AUTO_INCREMENT,
    ville VARCHAR(255),
    PRIMARY KEY(id_ville)
);


INSERT INTO villes_quebec (ville) VALUES
('Montréal'),
('Québec'),
('Laval'),
('Gatineau'),
('Longueuil'),
('Sherbrooke'),
('Saguenay'),
('Lévis'),
('Trois-Rivières'),
('Terrebonne'),
('Saint-Jean-sur-Richelieu'),
('Repentigny'),
('Brossard'),
('Drummondville'),
('Saint-Jérôme'),
('Granby'),
('Blainville'),
('Saint-Hyacinthe'),
('Dollard-des-Ormeaux'),
('Rimouski'),
('Châteauguay'),
('Saint-Eustache'),
('Victoriaville'),
('Rouyn-Noranda'),
('Salaberry-de-Valleyfield'),
('Boucherville'),
('Mirabel'),
('Sorel-Tracy'),
('Mascouche'),
('Côte-Saint-Luc'),
('Val-d\'Or'),
('Pointe-Claire'),
('Alma'),
('Saint-Georges'),
('Sainte-Julie'),
('Boisbriand'),
('Vaudreuil-Dorion'),
('Thetford Mines'),
('Sept-Îles'),
('Sainte-Thérèse'),
('La Prairie'),
('Saint-Bruno-de-Montarville'),
('Saint-Constant'),
('Magog'),
('Chambly'),
('Baie-Comeau'),
('Saint-Lambert'),
('Kirkland'),
('Joliette'),
('Victoriaville');


-- INSERT INTO conducteurs (co_id, co_nom, co_prenom, co_th, co_niv, co_qualification) VALUES (123, 'Bob', 'Bobby', 22.8, '1FAFP53U7XA192769', 'type 1'), (456, 'Gagnon', 'Garry', 20.5, 'JH4KA2630HC019837', 'type 2');

-- INSERT INTO mecanos (me_id, me_nom, me_prenom, me_th, me_qualification) VALUES (135, 'Tremblay', 'Réjean', 24.2, 'type 1'), (246, 'Roy', 'Nicolas', 20.5, 'type 3');

-- INSERT INTO serviceClient (sc_id, sc_nom, sc_prenom, sc_th, sc_langue) VALUES (987, 'Beaudoin', 'Carole', 20.0, 'FRA'), (789, 'Smith', 'Nicole', 21.0, 'ENG');

-- INSERT INTO vehicule (ve_niv, ve_immatriculation, ve_type_vehicule, ve_odometre, ve_mecanicienID) VALUES ('1FAHP3F20CL266328', 'AB123CD', 'type 2', 1500, 10), ('1FBHP3F20CL266328', 'EF456GH', 'type 3', 2700, 57);


DELIMITER //
CREATE PROCEDURE CreationVoyage()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE random_city1 VARCHAR(255);
    DECLARE random_city2 VARCHAR(255);
    WHILE i < 100 DO
        SELECT ville INTO random_city1 FROM villes_quebec ORDER BY RAND() LIMIT 1;
        SELECT ville INTO random_city2 FROM villes_quebec where villes_quebec.ville != random_city1 ORDER BY RAND() LIMIT 1;
        INSERT INTO voyage(vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest)
        VALUES (
            UUID(),
            FLOOR(RAND() * 111 + 10),
            NOW() + INTERVAL FLOOR(RAND() * 24) HOUR + INTERVAL FLOOR(RAND() * 365 + 1)DAY,
            random_city1,
            random_city2
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

