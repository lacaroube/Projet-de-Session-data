CREATE DATABASE agence_de_transport;
USE agence_de_transport;

CREATE TABLE IF NOT EXISTS ville (
    vi_nom varchar(20),
    vi_province char(2),
    vi_station varchar(20),
    primary key (vi_nom,vi_province)
);

CREATE TABLE IF NOT EXISTS vehicule (
    ve_niv varchar(17) primary key ,
    ve_immatriculation varchar(7) unique ,
    ve_type_vehicule enum('type 1','type 2','type 3') not null ,
    ve_odometre integer,
    ve_mecanicienID integer references mecanos(me_id)
);

CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur integer primary key,
    ut_username varchar(20),
    ut_password varchar(100),
    ut_nom varchar(20),
    ut_prenom varchar(20),
    ut_date_naissance date,
    ut_telephone varchar(10),
    ut_adresse varchar(100)
);

CREATE TABLE IF NOT EXISTS avis (
    no_avis integer primary key AUTO_INCREMENT,
    note enum('Excellent','Bien','Modeste','Mauvais','Aucune note'),
    commentaire varchar(200),
    id_utilisateur integer
    /*foreign key (id_utilisateur) REFERENCES utilisateur(id_utilisateur)*/
);

DROP TABLE avis;

CREATE TABLE IF NOT EXISTS voyage (
    vo_ni varchar(20) primary key,
    vo_prix_passager integer,
    vo_heure_dep DATETIME not null,
    vo_heure_arv DATETIME not null,
    vo_distance integer
);

CREATE TABLE IF NOT EXISTS employes (
    em_id integer primary key,
    em_nom varchar(20),
    em_prenom varchar(20),
    em_th FLOAT
);

CREATE TABLE IF NOT EXISTS conducteurs (
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
);

-- INSERT INTO conducteurs (co_id, co_nom, co_prenom, co_th, co_niv, co_qualification) VALUES (123, 'Bob', 'Bobby', 22.8, '1FAFP53U7XA192769', 'type 1'), (456, 'Gagnon', 'Garry', 20.5, 'JH4KA2630HC019837', 'type 2');

-- INSERT INTO mecanos (me_id, me_nom, me_prenom, me_th, me_qualification) VALUES (135, 'Tremblay', 'Réjean', 24.2, 'type 1'), (246, 'Roy', 'Nicolas', 20.5, 'type 3');

-- INSERT INTO serviceClient (sc_id, sc_nom, sc_prenom, sc_th, sc_langue) VALUES (987, 'Beaudoin', 'Carole', 20.0, 'FRA'), (789, 'Smith', 'Nicole', 21.0, 'ENG');

-- INSERT INTO vehicule (ve_niv, ve_immatriculation, ve_type_vehicule, ve_odometre, ve_mecanicienID) VALUES ('1FAHP3F20CL266328', 'AB123CD', 'type 2', 1500, 10), ('1FBHP3F20CL266328', 'EF456GH', 'type 3', 2700, 57);

-- INSERT INTO utilisateurs (id_utilisateur,ut_username,ut_password,ut_nom,ut_prenom,ut_date_naissance,ut_telephone,ut_adresse) VALUES (123,'test','123soleil','Joseph','Bobby','1990-3-17','1234567890','123 rue Deschamps');