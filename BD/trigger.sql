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
