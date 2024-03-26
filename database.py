import pymysql

connection = pymysql.connect(
    host='localhost',
    user="root",
    password="SdM4rs0laisC!",
    db="schema_name",
    autocommit=True
)

cursor = connection.cursor()


def insert_avis(text, note):
    cursor.execute(f"INSERT INTO avis (note, commentaire, id_utilisateur) VALUES ('{note}', '{text}', 1)")

