import os
from datetime import datetime, timedelta
import pymysql
import uuid

from flask import Response

from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return pymysql.connect(host=os.environ.get("HOST"),
                           user=os.environ.get("USER"),
                           password=os.environ.get("PASSWORD"),
                           db=os.environ.get("DATABASE"),
                           autocommit=True
                           )


def get_all_ville():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT ville FROM villes_quebec ORDER BY ville")
    result = cursor.fetchall()
    connection.close()
    return [row[0] for row in result]


def get_voyage(depart, destination, date_temps, prix):
    connection = get_db_connection()
    cursor = connection.cursor()
    date_temps_24 = datetime.strptime(date_temps, "%Y-%m-%dT%H:%M")
    date_temps_inf = date_temps_24 - timedelta(days=1)
    date_temps_sup = date_temps_24 + timedelta(days=1)
    print(date_temps_24)
    print(date_temps_inf)
    print(date_temps_sup)
    cursor.execute(f"SELECT vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager FROM voyage "
                   f"WHERE vo_dep = '{depart}' "
                   f"AND vo_dest = '{destination}' "
                   f"AND vo_heure_dep BETWEEN DATE('{date_temps_inf}') "
                   f"AND DATE('{date_temps_sup}') AND vo_prix_passager <= {prix};")
    result = cursor.fetchall()
    connection.close()
    return [{"vo_ni": vo_ni, "depart": depart, "destination": destination, "date_temps": date_temps, "prix": prix}
            for vo_ni, depart, destination, date_temps, prix in result]


def insert_avis(text, note, user_id, vo_ni):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO avis (vo_ni, note, commentaire, id_utilisateur)"
                   f"VALUES ('{vo_ni}', '{note}', '{text}', '{user_id}')")
    connection.close()


def insert_new_client(username, password, last_name, first_name, phone):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO utilisateurs (id_utilisateur,"
                   f"ut_username,"
                   f"ut_password,"
                   f"ut_nom,"
                   f"ut_prenom,"
                   f"ut_telephone)"
                   f"VALUES (UUID(),"
                   f"'{username}',"
                   f"'{password}',"
                   f"'{last_name}',"
                   f"'{first_name}',"
                   f"'{phone}')")
    cursor.execute("SELECT LAST_INSERT_ID()")
    utili_id = cursor.fetchone()[0]
    connection.close()
    return [utili_id, username, password, last_name, first_name, phone]


def insert_new_conducteur(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    myuuid = uuid.uuid4()
    cursor.execute(f"INSERT INTO conducteur (id_conducteur, username, password)"
                   f"VALUES ('{myuuid}', '{username}', '{password}');")
    connection.close()
    return [myuuid, username, password]


def insert_new_admin(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO admins (id_admin, adm_username, adm_password)"
                   f"VALUES (UUID(), '{username}', '{password}')")
    cursor.execute("SELECT LAST_INSERT_ID()")
    id = cursor.fetchone()[0]
    connection.close()
    return [id, username, password]


def get_avis(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT vo_ni, note, commentaire FROM avis WHERE id_utilisateur = '{user_id}'")
    result = cursor.fetchall()
    connection.close()
    return [{"vo_ni": vo_ni, "note": note, "commentaire": commentaire} for vo_ni, note, commentaire in result]


def supprime_avis(id_utilisateur, vo_ni):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM avis WHERE vo_ni = '{vo_ni}'"
                   f"AND id_utilisateur = '{id_utilisateur}'")
    connection.close()


def modifier_commentaire(id_utilisateur, vo_ni, text, note):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE avis SET commentaire = '{text}', note = '{note}'"
                   f"WHERE vo_ni = '{vo_ni}' AND id_utilisateur = '{id_utilisateur}'")
    connection.close()


def fetch_client(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE ut_username = %s", (username,))
    clients = cursor.fetchall()
    connection.close()
    return clients


def fetch_conducteur(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM conducteur WHERE username = %s", (username,))
    conducteurs = cursor.fetchall()
    connection.close()
    return conducteurs


def fetch_admin(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admins WHERE adm_username = %s", (username,))
    admins = cursor.fetchall()
    connection.close()
    return admins


def insert_voyage(departure, destination, days, hour, price):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.callproc("InsertVoyage", (departure, destination, price, hour, days))
    connection.close()


def insert_new_voyage_utilisateur(vo_ni, id_utilisateur):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO voyage_utilisateur (vo_ni, id_utilisateur) VALUES "
                   f"('{vo_ni}', '{id_utilisateur}')")
    connection.close()


def get_voyages_user(id_utilisateur):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT v.vo_ni, v.vo_dep, v.vo_dest, v.vo_heure_dep, v.vo_prix_passager "
                   f"FROM voyage_utilisateur vu JOIN voyage v ON vu.vo_ni = v.vo_ni "
                   f"WHERE vu.id_utilisateur = '{id_utilisateur}'")
    voyages = cursor.fetchall()
    connection.close()
    return [{"vo_ni": vo_ni, "vo_dep": vo_dep, "vo_dest": vo_dest,
             "vo_heure_dep": vo_heure_dep, "vo_prix_passager": vo_prix_passager}
            for vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager in voyages]


def delete_voyage_user(id_utilisateur, vo_ni):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM voyage_utilisateur WHERE id_utilisateur = '{id_utilisateur}' AND vo_ni = '{vo_ni}'")
    connection.close()


def fetch_horaire_conducteur(id_conducteur, date):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT heure_debut, heure_fin, conger FROM horaire_conducteur "
                   f" WHERE id_conducteur = '{id_conducteur}' AND date = DATE('{date}') AND conger !=TRUE")
    result = cursor.fetchall()
    connection.close()
    if len(result) == 0:
        return result
    return [{"heure_debut": str(heure_debut), "heure_fin": str(heure_fin), "conger": conger}
            for heure_debut, heure_fin, conger in result]


def insert_day_off(id_conducteur, date):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT voyage_av_midi, voyage_ap_midi, conger FROM horaire_conducteur "
                   f"WHERE id_conducteur = '{id_conducteur}' "
                   f"AND date = DATE('{date}')")
    conducteur_occupe = cursor.fetchone()
    connection.close()
    if conducteur_occupe[2] == 1:
        raise ValueError("L'utilisateur est deja en conger")

    new_conducteurs_id = []
    if conducteur_occupe[0] == 1 or conducteur_occupe[1] == 1:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT vo_ni FROM voyage "
                       f"WHERE id_conducteur = '{id_conducteur}' "
                       f"AND date = DATE('{date}')")
        voyages_trouves = cursor.fetchall()
        connection.close()
        for voyage_id in voyages_trouves:
            cursor = connection.cursor()
            try:
                cursor.callproc("DemandeDeConger", (voyage_id, id_conducteur))
                returned_id = cursor.fetchone()
                new_conducteurs_id.append(returned_id[0])
            except Exception:
                raise Exception("Ceci est une autre type d'erreur")

        if len(new_conducteurs_id) == len(voyages_trouves):
            try:
                prise_de_conge(id_conducteur)
                accepted_conger(id_conducteur, date)
                new_conducteur_voyage(voyages_trouves, new_conducteurs_id)
            except Exception:
                raise Exception("Ceci est une autre type d'erreur")
    else:
        try:
            prise_de_conge(id_conducteur)
        except Exception as e:
            raise Exception(f"Ceci est une autre type d'erreur : %s", e)

        try:
            accepted_conger(id_conducteur, date)
        except Exception as e:
            raise Exception(f"Ceci est une autre type d'erreur : %s", e)


def new_conducteur_voyage(voyages, new_conducteurs_id):
    numero_utilisateur = 0
    for voyage_id in voyages:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"UPDATE voyage SET id_conducteur = '{new_conducteurs_id[numero_utilisateur]}' WHERE vo_ni = '{voyage_id}';")
        numero_utilisateur += 1
        connection.close()


def accepted_conger(id_conducteur, date):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE horaire_conducteur "
                   f"SET conger = TRUE, voyage_av_midi = FALSE, voyage_ap_midi = FALSE "
                   f"WHERE id_conducteur = '{id_conducteur}' "
                   f"AND date = DATE('{date}')")
    connection.close()


def prise_de_conge(id_conducteur):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT nb_jour_conger FROM conducteur WHERE id_conducteur = '{id_conducteur}'")
    nb_jours = cursor.fetchone()
    connection.close()
    if nb_jours[0] > 0:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE conducteur SET nb_jour_conger = '{nb_jours[0] - 1}'"
                       f"WHERE id_conducteur = '{id_conducteur}'")
        connection.close()

    else:
        raise TypeError("L'utilisateur n'a plus de jour de conger")


def get_voyages_conducteur(id_conducteur, date):
    heure_min = datetime.strptime(date, "%Y-%m-%d")
    heure_max = heure_min + timedelta(days=1)
    print(heure_min.date(), heure_max.date())
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager "
                   f"FROM voyage "
                   f"WHERE id_conducteur = '{id_conducteur}' "
                   f"AND vo_heure_dep BETWEEN '{heure_min.date()}' AND '{heure_max.date()}' "
                   f"ORDER BY vo_heure_dep")
    result = cursor.fetchall()
    connection.close()
    return [{"vo_ni": vo_ni, "depart": vo_dep, "destination": vo_dest, "date_temps": vo_heure_dep, "prix": vo_prix_passager}
            for vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager in result]
