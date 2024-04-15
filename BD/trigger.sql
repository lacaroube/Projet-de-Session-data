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

/*
DELIMITER //
CREATE TRIGGER check_si_conducteur_disponible
BEFORE INSERT ON voyage
FOR EACH ROW
BEGIN
    DECLARE nb_conducteur INT DEFAULT 0;
    IF(DATE_FORMAT(NEW.vo_heure_dep, '%H:%i:%s') < TIME('12:00:00')) THEN
        SELECT COUNT(*) INTO nb_conducteur FROM horaire_conducteur H, voyage V
                                           WHERE H.date = DATE(v.vo_heure_dep) AND H.heure_debut <= TIME(V.vo_heure_dep)
                                             AND H.heure_fin > TIME(V.vo_heure_dep) AND H.voyage_av_midi = false AND H.conger = false;
    END IF;

   IF(DATE_FORMAT(NEW.vo_heure_dep, '%H:%i:%s') >= TIME('12:00:00')) THEN
        SELECT COUNT(*) INTO nb_conducteur FROM horaire_conducteur H, voyage V
                                           WHERE H.date = DATE(v.vo_heure_dep) AND H.heure_debut <= TIME(V.vo_heure_dep)
                                             AND H.heure_fin > TIME(V.vo_heure_dep) AND H.voyage_ap_midi = false AND H.conger = false;
    END IF;

    IF nb_conducteur = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Aucun horaire de conducteur est disponible pour cette date et cette heure';
    END IF;
END;
//
DELIMITER ;*/




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
