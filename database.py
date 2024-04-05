import os
from datetime import datetime, timedelta
import pymysql

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
    cursor.execute(f"SELECT * FROM voyage WHERE vo_dep = '{depart}' "
                   f"AND vo_dest = '{destination}' "
                   f"AND vo_heure_dep BETWEEN '{date_temps_inf}' "
                   f"AND '{date_temps_sup}' AND vo_prix_passager <= {prix};")
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


def fetch_admin(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admins WHERE adm_username = %s", (username,))
    admins = cursor.fetchall()
    connection.close()
    return admins


def insert_voyage(departure, destination, date_time, price):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO voyage (vo_ni,"
                   f"vo_prix_passager,"
                   f"vo_heure_dep,"
                   f"vo_dep,"
                   f"vo_dest)"
                   f"VALUES (UUID(),"
                   f"'{price}',"
                   f"'{date_time}',"
                   f"'{departure}',"
                   f"'{destination}');")
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
    cursor.execute(f"SELECT v.* FROM voyage_utilisateur vu JOIN voyage v ON vu.vo_ni = v.vo_ni "
                   f"WHERE vu.id_utilisateur = '{id_utilisateur}'")
    voyages = cursor.fetchall()
    connection.close()
    return [{"vo_ni": vo_ni, "vo_prix_passager": vo_prix_passager, "vo_heure_dep": vo_heure_dep, "vo_dep": vo_dep, "vo_dest": vo_dest}
            for vo_ni, vo_prix_passager, vo_heure_dep, vo_dep, vo_dest in voyages]


def delete_voyage_user(id_utilisateur, vo_ni):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM voyage_utilisateur WHERE id_utilisateur = '{id_utilisateur}' AND vo_ni = '{vo_ni}'")
    connection.close()
