import pymysql

connection = pymysql.connect(
    host='localhost',
    user="root",
    password="SdM4rs0laisC!",
    db="agence_de_transport",
    autocommit=True
)

cursor = connection.cursor()


def insert_avis(text):
    cursor.execute(f"INSERT INTO avis (commentaire) VALUES ('{text}')")

