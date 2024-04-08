insert INTO villes_quebec (ville) VALUES
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

DELIMITER //
CREATE TRIGGER check_si_conducteur_disponible
BEFORE INSERT ON voyage
FOR EACH ROW
BEGIN
    DECLARE nb_conducteur INT DEFAULT 0;
    IF(DATE_FORMAT(NEW.vo_heure_dep, '%H:%i:%s') < TIME('12:00:00')) THEN
        SELECT COUNT(*) INTO nb_conducteur FROM horaire_conducteur H, voyage V
                                           WHERE H.date = DATE(v.vo_heure_dep) AND H.heure_debut <= TIME(V.vo_heure_dep)
                                             AND H.heure_fin > TIME(V.vo_heure_dep) AND H.voyage_av_midi = false;
    END IF;

   IF(DATE_FORMAT(NEW.vo_heure_dep, '%H:%i:%s') >= TIME('12:00:00')) THEN
        SELECT COUNT(*) INTO nb_conducteur FROM horaire_conducteur H, voyage V
                                           WHERE H.date = DATE(v.vo_heure_dep) AND H.heure_debut <= TIME(V.vo_heure_dep)
                                             AND H.heure_fin > TIME(V.vo_heure_dep) AND H.voyage_ap_midi = false;
    END IF;

    IF nb_conducteur = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aucun horaire de conducteur est disponible pour cette date et cette heure';
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER checkConducteurUsername
BEFORE INSERT ON conducteur
FOR EACH ROW
BEGIN
    DECLARE username_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO username_exists FROM conducteur WHERE username = NEW.username;

    IF username_exists != 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le username est deja pris';
    END IF;
END;
//
DELIMITER ;




DELIMITER //
CREATE PROCEDURE InsertVoyage(IN dep VARCHAR(255), IN dest VARCHAR(255), IN price INT, IN hours INT, IN days INT)
    BEGIN
        INSERT INTO voyage(vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest)
        VALUES (
            UUID(),
            price,
            NOW() + INTERVAL hours HOUR + INTERVAL days DAY,
            dep,
            dest
        );
    END;
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CreationVoyage()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE j INT DEFAULT 0;
    DECLARE random_city1 VARCHAR(255);
    DECLARE random_city2 VARCHAR(255);
    DECLARE random_city3 VARCHAR(255);

    WHILE i < 100 DO
        SELECT ville INTO random_city1 FROM villes_quebec ORDER BY RAND() LIMIT 1;
        SELECT ville INTO random_city2 FROM villes_quebec where villes_quebec.ville != random_city1 ORDER BY RAND() LIMIT 1;
        SELECT ville INTO random_city3 FROM villes_quebec WHERE villes_quebec.ville != 'Montréal' AND villes_quebec.ville != 'Québec' ORDER BY RAND() LIMIT 1;
        CALL InsertVoyage(random_city1, random_city2, FLOOR(RAND() * 111 + 10), FLOOR(RAND() * 24), FLOOR(RAND() * 365 + 1));
        CALL InsertVoyage('Montréal', random_city3, FLOOR(RAND() * 111 + 10), FLOOR(RAND() * 24), FLOOR(RAND() * 365 + 1));
        SET i = i + 1;

    END WHILE;

    WHILE j < 365 DO
      CALL InsertVoyage('Montréal', 'Québec', FLOOR(RAND() * 20 + 100), 11, j);
        CALL InsertVoyage('Québec', 'Montréal', FLOOR(RAND() * 20 + 100), 11, j);
        CALL InsertVoyage('Montréal', 'Québec', FLOOR(RAND() * 20 + 100), 17, j);
        CALL InsertVoyage('Québec', 'Montréal', FLOOR(RAND() * 20 + 100), 17, j);

        SET j = j + 1;
    END WHILE;

END //
DELIMITER ;

CALL CreationVoyage();

DELIMITER //
CREATE PROCEDURE PopulateConducteur(IN num_rows INT)
BEGIN
 DECLARE i INT DEFAULT 0;
 DECLARE random_id VARCHAR(36);
 DECLARE random_username VARCHAR(20);
 DECLARE random_password VARCHAR(200);
 DECLARE j INT DEFAULT 0;

 WHILE i < num_rows DO
     SET random_id = UUID();
     SET random_username = CONCAT('user', LPAD(i, 5, '0'));
     SET random_password = SHA2(CONCAT('password', LPAD(i, 5, '0')), 256);

     INSERT INTO conducteur(id_conducteur, username, password)
     VALUES (random_id, random_username, random_password);

     WHILE j < 365 DO
         INSERT INTO horaire_conducteur(id_conducteur, date, heure_debut, heure_fin)
         VALUES (random_id, DATE_ADD(CURDATE(), INTERVAL j DAY), TIME('09:00:00'), TIME('18:00:00'));
         SET j = j + 1;
         END WHILE;

     SET j = 0;
     SET i = i + 1;

     END WHILE;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER assigner_horaire AFTER INSERT ON conducteur
FOR EACH ROW
    BEGIN
        DECLARE j INT DEFAULT 0;

        WHILE j < 365 DO

            INSERT INTO horaire_conducteur(id_conducteur, date, heure_debut, heure_fin)
            VALUES (NEW.id_conducteur, DATE_ADD(CURDATE(), INTERVAL j DAY), TIME('09:00:00'), TIME('18:00:00'));

            SET j = j + 1;
        END WHILE;
END //
DELIMITER ;

CALL PopulateConducteur(35);

DROP PROCEDURE PopulateConducteur;

SELECT * FROM horaire_conducteur;

SELECT * FROM conducteur;

INSERT INTO horaire_conducteur(id_conducteur, date, heure_debut, heure_fin)
VALUES ('a01edd57-f5b5-11ee-bbbe-309c23e5e88b', DATE_ADD(CURDATE(), INTERVAL 1 DAY), TIME('09:00:00'), TIME('18:00:00'))


-- INSERT INTO voyage(vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest) VALUES (UUID(), 50, '2024-05-14 09:59:47', 'Chambly', 'Saint-Hyacinthe');