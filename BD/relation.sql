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
CREATE PROCEDURE InsertVoyage(IN dep VARCHAR(255), IN dest VARCHAR(255), IN price INT, IN heure INT, IN jour INT)
    BEGIN
        DECLARE conducteur_voyage_id varchar(36);
        DECLARE date_voulu DATE;
        DECLARE heure_voulu TIME;
        DECLARE random_username VARCHAR(60);
        DECLARE random_password VARCHAR(200);

        SET date_voulu= DATE(NOW() + INTERVAL jour DAY);
        SET heure_voulu = MAKETIME(heure, 0, 0);

        IF(heure_voulu < TIME('12:00:00')) THEN
            SELECT H.id_conducteur INTO conducteur_voyage_id FROM horaire_conducteur H
            WHERE H.date = date_voulu AND H.conger = FALSE AND H.voyage_av_midi = FALSE
            ORDER BY (SELECT COUNT(*) FROM voyage V where V.id_conducteur = H.id_conducteur)
            LIMIT 1;
        END IF;

        IF(heure_voulu >= TIME('12:00:00')) THEN
            SELECT H.id_conducteur INTO conducteur_voyage_id FROM horaire_conducteur H
            WHERE H.date = date_voulu AND H.conger = FALSE AND H.voyage_ap_midi = FALSE
            ORDER BY (SELECT COUNT(*) FROM voyage V where V.id_conducteur = H.id_conducteur)
            LIMIT 1;
        END IF;

        IF conducteur_voyage_id IS NULL THEN
            SET conducteur_voyage_id = UUID();
            SET random_username = CONCAT('user', conducteur_voyage_id);
            SET random_password = SHA2(CONCAT('password', conducteur_voyage_id), 256);
            INSERT INTO conducteur(id_conducteur, username, password)
            VALUES (conducteur_voyage_id, random_username, random_password);
        END IF;

          IF(heure_voulu < TIME('12:00:00')) THEN
            UPDATE horaire_conducteur H SET voyage_av_midi = TRUE WHERE H.id_conducteur = conducteur_voyage_id AND H.date=date_voulu;
        END IF;

        IF(heure_voulu >= TIME('12:00:00')) THEN
            UPDATE horaire_conducteur H SET voyage_ap_midi = TRUE WHERE H.id_conducteur = conducteur_voyage_id AND H.date=date_voulu;
        END IF;

        INSERT INTO voyage(vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest, id_conducteur)
        VALUES (
            UUID(),
            price,
            TIMESTAMP(date_voulu, heure_voulu),
            dep,
            dest,
            conducteur_voyage_id
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

    WHILE i < 650 DO
        SELECT ville INTO random_city1 FROM villes_quebec ORDER BY RAND() LIMIT 1;
        SELECT ville INTO random_city2 FROM villes_quebec where villes_quebec.ville != random_city1 ORDER BY RAND() LIMIT 1;
        SELECT ville INTO random_city3 FROM villes_quebec WHERE villes_quebec.ville != 'Montréal' AND villes_quebec.ville != 'Québec' ORDER BY RAND() LIMIT 1;
        CALL InsertVoyage(random_city1, random_city2, FLOOR(RAND() * 111 + 10), FLOOR(RAND() * 9) + 9, FLOOR(RAND() * 365 + 1));
        CALL InsertVoyage('Montréal', random_city3, FLOOR(RAND() * 111 + 10), FLOOR(RAND() * 9) + 9, FLOOR(RAND() * 365 + 1));
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

DELIMITER //
CREATE PROCEDURE DemandeDeConger( IN voyage_ni varchar(36), IN old_id_conducteur varchar(36), OUT new_conducteur varchar(36))
BEGIN
    DECLARE jour DATE;
    DECLARE heure TIME;
    SELECT vo_heure_dep INTO jour FROM voyage V WHERE V.vo_ni = voyage_ni;
    SELECT vo_heure_dep INTO heure FROM voyage V WHERE V.vo_ni = voyage_ni;

    IF(DATE_FORMAT(heure, '%H:%i:%s') < TIME('12:00:00')) THEN
        SELECT H.id_conducteur INTO new_conducteur FROM horaire_conducteur H
        WHERE date = jour AND conger = FALSE AND voyage_av_midi = FALSE AND H.id_conducteur != old_id_conducteur
        LIMIT 1;
    END IF;

        IF(DATE_FORMAT(heure, '%H:%i:%s') >= TIME('12:00:00')) THEN
        SELECT id_conducteur INTO new_conducteur FROM horaire_conducteur
        WHERE date = jour AND conger = FALSE AND voyage_ap_midi = FALSE AND id_conducteur != old_id_conducteur
        LIMIT 1;
    END IF;

    IF new_conducteur IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aucun conducteur remplaçant disponible pour cette journée.';
    END IF;

END //
DELIMITER ;

CALL CreationVoyage();


SELECT * FROM voyage WHERE id_conducteur = '841450f2-56d6-452d-8599-66cd95bbeb5c';

SELECT * FROM horaire_conducteur WHERE id_conducteur='841450f2-56d6-452d-8599-66cd95bbeb5c';

SELECT * FROM conducteur WHERE id_conducteur='841450f2-56d6-452d-8599-66cd95bbeb5c';

SELECT * FROM utilisateurs;

UPDATE horaire_conducteur SET conger = FALSE, voyage_av_midi = FALSE, voyage_ap_midi = FALSE
                          WHERE id_conducteur = '841450f2-56d6-452d-8599-66cd95bbeb5c' AND date = DATE('2024-04-29');

SELECT * FROM voyage WHERE vo_dep = 'Montreal'
AND vo_dest = 'Quebec'
AND vo_heure_dep BETWEEN DATE('2024-04-27 11:08:00') AND DATE('2024-04-28 11:08:00')
AND vo_prix_passager <= 120;

INSERT INTO conducteur(id_conducteur, username, password) VALUES(UUID(), 'userConger', '1234');
-- INSERT INTO voyage(vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest) VALUES (UUID(), 50, '2024-05-14 09:59:47', 'Chambly', 'Saint-Hyacinthe');