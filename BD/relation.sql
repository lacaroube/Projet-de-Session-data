CREATE TABLE conduite(
    conducteurId integer,
    vehiculeId varchar(17),
    PRIMARY KEY(conducteurId, vehiculeID),
    FOREIGN KEY (conducteurId) REFERENCES conducteurs(co_id),
    FOREIGN KEY (vehiculeID) REFERENCES vehicule(ve_niv)
);

DROP TABLE conduite;

CREATE TABLE assistance(
    serviceClientId integer,
    id_utilisateur integer,
    timeOfAssistance DATETIME not null,
    avisUtilisateurNo integer,
    PRIMARY KEY (serviceClientId, id_utilisateur, timeOfAssistance),
    FOREIGN KEY (serviceClientId) REFERENCES serviceclient(sc_id),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (avisUtilisateurNo) REFERENCES avis(no_avis)
);

CREATE TABLE participationUtilisateurs (
    niVoyage varchar(20),
    niUtilisateur integer,
    PRIMARY KEY (niUtilisateur),
    FOREIGN KEY (niVoyage) REFERENCES voyage(vo_ni),
    FOREIGN KEY (niUtilisateur) REFERENCES utilisateur(id_utilisateur)
);

DROP TABLE participationUtilisateurs;


CREATE TABLE utilisateurs_avis (
    uaUtilisateur integer,
    uaAvis integer,
    PRIMARY KEY (uaUtilisateur),
    FOREIGN KEY (uaAvis) REFERENCES avis (no_avis)
);
DROP TABLE utilisateurs_avis;

CREATE TABLE participationVehicules (
    niVehicule varchar(17),
    niVoyage varchar(20),
    PRIMARY KEY (niVehicule),
    FOREIGN KEY (niVehicule) REFERENCES vehicule(ve_niv),
    FOREIGN KEY (niVoyage) REFERENCES voyage(vo_ni)
);

-- TODO relation 8 a voir si integrer dans voyage ou non

