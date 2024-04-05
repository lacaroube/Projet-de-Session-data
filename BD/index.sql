CREATE DATABASE agence_de_transport;
USE agence_de_transport;


CREATE TABLE IF NOT EXISTS vehicule (
    ve_niv varchar(17) primary key ,
    ve_immatriculation varchar(7) unique ,
    ve_type_vehicule enum('type 1','type 2','type 3') not null ,
    ve_odometre integer
    /* ve_mecanicienID integer references mecanos(me_id) */
);

CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur varchar(36) primary key,
    ut_username varchar(20),
    ut_password varchar(200),
    ut_nom varchar(20),
    ut_prenom varchar(20),
    ut_telephone varchar(10)
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
    vo_dest varchar(255)
);

INSERT INTO voyage(vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest) VALUES (UUID(), 50, '2024-05-14 09:59:47', 'Chambly', 'Saint-Hyacinthe');


CREATE TABLE IF NOT EXISTS admins (
    id_admin varchar(36) primary key,
    adm_username varchar(20),
    adm_password varchar(200)
);

/* CREATE TABLE IF NOT EXISTS conducteurs (
    co_id integer primary key references employes (em_id),
    co_nom varchar(20) references employes (em_nom),
    co_prenom varchar(20) references employes (em_prenom),
    co_th FLOAT references employes (em_th),
    co_niv varchar(17) references vehicule(ve_niv) ,
    co_qualification enum('type 1','type 2','type 3') not null references vehicule (ve_type_vehicule)
);

CREATE TABLE IF NOT EXISTS mecanos (
    me_id integer primary key references employes (em_id),
    me_nom varchar(20) references employes (em_nom),
    me_prenom varchar(20) references employes (em_prenom),
    me_th FLOAT references employes (em_th),
    me_qualification enum('type 1','type 2','type 3') not null references vehicule (ve_type_vehicule)
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

CALL CreationVoyage();


DELIMITER //
CREATE TRIGGER check_ville_quebec
BEFORE INSERT ON voyage
FOR EACH ROW
BEGIN
    DECLARE dep_exists INT;
    DECLARE dest_exists INT;

    SELECT COUNT(*) INTO dep_exists FROM villes_quebec WHERE ville = NEW.vo_dep;
    SELECT COUNT(*) INTO dest_exists FROM villes_quebec WHERE ville = NEW.vo_dest;

    IF dep_exists = 0 OR dest_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Les villes de départ et de destination doivent être des villes du Québec.';
    END IF;
END;
//
DELIMITER ;
