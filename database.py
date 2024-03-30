from datetime import datetime, timedelta
import pymysql


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user="root",
                           password="SdM4rs0laisC!",
                           db="agence_de_transport",
                           autocommit=True
                           )


def get_all_ville():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT ville FROM villes_quebec")
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


def insert_avis(text, note):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO avis (note, commentaire, id_utilisateur) VALUES ('{note}', '{text}', 1)")
    connection.close()


def insert_new_client(id, username, password, last_name, first_name, birth_date, phone, address):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO utilisateurs (id_utilisateur,ut_username,"
                   f"ut_password,"
                   f"ut_nom,"
                   f"ut_prenom,"
                   f"ut_date_naissance,"
                   f"ut_telephone,"
                   f"ut_adresse)"
                   f"VALUES ('{id}',"
                   f"'{username}',"
                   f"'{password}',"
                   f"'{last_name}',"
                   f"'{first_name}',"
                   f"'{birth_date}',"
                   f"'{phone}',"
                   f"'{address}')")
    connection.close()


def get_avis():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT no_avis, note, commentaire FROM avis WHERE id_utilisateur = 1")
    result = cursor.fetchall()
    connection.close()
    return [{"no_avis": no_avis, "note": note, "commentaire": commentaire} for no_avis, note, commentaire in result]


def supprime_avis(no_avis):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM avis WHERE no_avis = {no_avis}")
    connection.close()


def modifierCommentaire(no_avis, text, note):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE avis SET commentaire = '{text}', note = '{note}'"
                   f"WHERE id_utilisateur = 1 AND no_avis = {no_avis}")
    connection.close()


def fetch_client(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE ut_username = %s", (username,))
    clients = cursor.fetchall()
    connection.close()
    return clients
