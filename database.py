import pymysql


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user="root",
                           password="SdM4rs0laisC!",
                           db="agence_de_transport",
                           autocommit=True
                           )


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


def fetch_client(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE ut_username = %s", (username,))
    clients = cursor.fetchall()
    connection.close()

    return clients
