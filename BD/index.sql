CREATE DATABASE agence_de_transport;
USE agence_de_transport;


CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur varchar(36) primary key,
    ut_username varchar(20),
    ut_password varchar(200),
    ut_nom varchar(20),
    ut_prenom varchar(20),
    ut_date_naissance date,
    ut_telephone varchar(10),
    ut_adresse varchar(100)
);

CREATE TABLE IF NOT EXISTS avis (
    no_avis integer AUTO_INCREMENT,
    note enum('Excellent','Bien','Modeste','Mauvais','Aucune note'),
    commentaire varchar(200),
    id_utilisateur varchar(36),
    PRIMARY KEY (no_avis, id_utilisateur),
    foreign key (id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
);

CREATE TABLE IF NOT EXISTS voyage (
    vo_ni varchar(36) primary key,
    vo_prix_passager integer,
    vo_heure_dep DATETIME not null,
    vo_dep varchar(255),
    vo_dest varchar(255)
);


CREATE TABLE IF NOT EXISTS admins (
    id_admin varchar(36) primary key,
    adm_username varchar(20),
    adm_password varchar(200)
);


CREATE TABLE IF NOT EXISTS villes_quebec (
    id_ville INT AUTO_INCREMENT,
    ville VARCHAR(255),
    PRIMARY KEY(id_ville)
);

CREATE TABLE IF NOT EXISTS voyage_utilisateur(
    id_participation integer AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur varchar(36),
    vo_ni varchar(36),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur),
    FOREIGN KEY (vo_ni) REFERENCES voyage(vo_ni)
);

CREATE TABLE IF NOT EXISTS conducteur(
    id_conducteur varchar(36) PRIMARY KEY,
    username varchar(20),
    password varchar(200),
    nb_jour_conger INT DEFAULT 28
);

CREATE TABLE IF NOT EXISTS horaire_conducteur(
    id_conducteur varchar(36),
    date DATE,
    heure_debut TIME,
    heure_fin TIME,
    voyage_av_midi BOOL DEFAULT FALSE,
    voyage_ap_midi BOOL DEFAULT FALSE,
    PRIMARY KEY (id_conducteur, date),
    FOREIGN KEY (id_conducteur) REFERENCES conducteur(id_conducteur)
);

DROP TABLE horaire_conducteur;
