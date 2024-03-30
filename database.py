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
    date_temps_inf = date_temps - datetime.timedelta(days=1)
    date_temps_sup = date_temps + datetime.timedelta(days=1)
    cursor.execute(f"SELECT * FROM voyage WHERE vo_dep = '{depart}' "
                   f"AND vo_dest = '{destination}' "
                   f"AND vo_heure_dep BETWEEN '{date_temps_inf}' "
                   f"AND '{date_temps_sup}' AND vo_prix_passager <= {prix};")
    result = cursor.fetchall()
    return result


def insert_avis(text, note, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO avis (note, commentaire, id_utilisateur) VALUES ('{note}', '{text}', '{user_id}')")
    connection.close()


def insert_new_client(username, password, last_name, first_name, birth_date, phone, address):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO utilisateurs (id_utilisateur,"
                   f"ut_username,"
                   f"ut_password,"
                   f"ut_nom,"
                   f"ut_prenom,"
                   f"ut_date_naissance,"
                   f"ut_telephone,"
                   f"ut_adresse)"
                   f"VALUES (UUID(),"
                   f"'{username}',"
                   f"'{password}',"
                   f"'{last_name}',"
                   f"'{first_name}',"
                   f"'{birth_date}',"
                   f"'{phone}',"
                   f"'{address}')")
    cursor.execute("SELECT LAST_INSERT_ID()")
    id = cursor.fetchone()[0]
    connection.close()
    return [id, username, password, last_name, first_name, birth_date, phone, address]


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
    cursor.execute(f"SELECT no_avis, note, commentaire FROM avis WHERE id_utilisateur = '{user_id}'")
    result = cursor.fetchall()
    connection.close()
    return [{"no_avis": no_avis, "note": note, "commentaire": commentaire} for no_avis, note, commentaire in result]


def supprime_avis(no_avis):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM avis WHERE no_avis = '{no_avis}'")
    connection.close()


def modifier_commentaire(no_avis, text, note):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE avis SET commentaire = '{text}', note = '{note}'"
                   f"WHERE no_avis = '{no_avis}'")
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
