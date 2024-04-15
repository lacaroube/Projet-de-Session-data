import os
from datetime import datetime, timedelta
import pymysql
import uuid

from flask import Response

from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        load_dotenv()
        self.host = os.environ.get("HOST")
        self.port = int(os.environ.get("PORT"))
        self.database = os.environ.get("DATABASE")
        self.user = os.environ.get("USER")
        self.password = os.environ.get("PASSWORD")

        self._get_connection()

    def _get_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True
        )

        self.cursor = self.connection.cursor()

    ''' Cette fonction permet l'obtention de la liste de toutes les villes de Québec
        SORTIE : La liste de toutes les villes de Québec'''
    def get_all_ville(self):
        self.cursor.execute("SELECT ville FROM villes_quebec ORDER BY ville")
        result = self.cursor.fetchall()
        self.connection.close()
        return [row[0] for row in result]

    ''' Cette fonction permet d'obtenir une liste de voyages suivant des critères précis
        ENTREE : Le lieu de départ du voyage, sa destination l'heure de départ, ainsi que le prix maximal
        SORTIE : La liste des voyages respectant ces critères dans un intervalle de 24h avant et après la date indiquée'''
    def get_voyage(self, depart, destination, date_temps, prix):
        date_temps_24 = datetime.strptime(date_temps, "%Y-%m-%dT%H:%M")
        date_temps_inf = date_temps_24 - timedelta(days=1)
        date_temps_sup = date_temps_24 + timedelta(days=1)
        self.cursor.execute(f"SELECT vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager FROM voyage "
                            f"WHERE vo_dep = '{depart}' "
                            f"AND vo_dest = '{destination}' "
                            f"AND vo_heure_dep BETWEEN DATE('{date_temps_inf}') "
                            f"AND DATE('{date_temps_sup}') AND vo_prix_passager <= {prix};")
        result = self.cursor.fetchall()
        self.connection.close()
        return [{"vo_ni": vo_ni, "depart": depart, "destination": destination, "date_temps": date_temps, "prix": prix}
                for vo_ni, depart, destination, date_temps, prix in result]

    ''' Cette fonction permet l'ajout de nouveaux avis.
        ENTREE : Le commmentaire, la note, l'identifiant de l'utilisateur, ainsi que le 
        numéro d'identification du voyage.
        SORTIE : Rien'''
    def insert_avis(self, text, note, user_id, vo_ni):
        self.cursor.execute(f"INSERT INTO avis (vo_ni, note, commentaire, id_utilisateur)"
                            f"VALUES ('{vo_ni}', '{note}', '{text}', '{user_id}')")
        self.connection.close()

    ''' Cette fonction permet l'insertion d'un nouveau client dans la base de données.
        ENTREE : Le nom d'utilisateur, le mot de passe, le nom, le prénom et le numéro
        de téléphone du client.
        SORTIE : Les informations entrées par l'utilisateur'''
    def insert_new_client(self, username, password, last_name, first_name, phone):
        myuuid = uuid.uuid4()
        self.cursor.execute(f"INSERT INTO utilisateurs (id_utilisateur,"
                            f"ut_username,"
                            f"ut_password,"
                            f"ut_nom,"
                            f"ut_prenom,"
                            f"ut_telephone)"
                            f"VALUES ('{myuuid}',"
                            f"'{username}',"
                            f"'{password}',"
                            f"'{last_name}',"
                            f"'{first_name}',"
                            f"'{phone}')")
        return [myuuid, username, password, last_name, first_name, phone]

    ''' Cette fonction permet l'insertion d'un nouveau conducteur.
        ENTREE : Le nom d'utilisateur et le mot de passe du conducteur.
        SORTIE : Les informations entrées par le conducteur ainsi que l'uid qui lui est attribué.'''
    def insert_new_conducteur(self, username, password):
        myuuid = uuid.uuid4()
        self.cursor.execute(f"INSERT INTO conducteur (id_conducteur, username, password)"
                            f"VALUES ('{myuuid}', '{username}', '{password}');")
        self.connection.close()
        return [myuuid, username, password]

    ''' Cette fonction permet le rajout d'un nouvel admin.
        ENTREE : Le nom d'utilisateur et le mot de passe de l'admin.
        SORTIE : Les informations entrées par l'admin ainsi que l'ID qui lui est attribué.'''
    def insert_new_admin(self, username, password):
        myuuid = uuid.uuid4()
        self.cursor.execute(f"INSERT INTO admins (id_admin, adm_username, adm_password)"
                            f"VALUES ('{myuuid}', '{username}', '{password}')")
        return [myuuid, username, password]

    ''' Cette fonction permet l'obtention des avis d'un utilisateur grâce à son ID.
        ENTREE : L'ID de l'utilisateur dont on veut obtenir les avis.
        SORTIE : Les différents avis de l'utilisateur en question (NI, note et commentaire et l'avis).'''
    def get_avis(self, user_id):
        self.cursor.execute(f"SELECT vo_ni, note, commentaire FROM avis WHERE id_utilisateur = '{user_id}'")
        result = self.cursor.fetchall()
        self.connection.close()
        return [{"vo_ni": vo_ni, "note": note, "commentaire": commentaire} for vo_ni, note, commentaire in result]

    ''' Cette fonction permet la suppression de l'avis d'un utilisateur.
        ENTREE : ID de l'utilisateur et numéro d'identification de l'avis.
        SORTIE : Rien.'''
    def supprime_avis(self, id_utilisateur, vo_ni):
        self.cursor.execute(f"DELETE FROM avis WHERE vo_ni = '{vo_ni}'"
                            f"AND id_utilisateur = '{id_utilisateur}'")
        self.connection.close()

    ''' Cette fonction permet la modification d'un avis.
        ENTREE : ID de l'utilisateur, NI, commentaire et note de l'avis.
        SORTIE : Rien.'''
    def modifier_commentaire(self, id_utilisateur, vo_ni, text, note):
        self.cursor.execute(f"UPDATE avis SET commentaire = '{text}', note = '{note}'"
                            f"WHERE vo_ni = '{vo_ni}' AND id_utilisateur = '{id_utilisateur}'")
        self.connection.close()

    ''' Cette fonction permet l'obtention d'une liste d'utilisateur.
        ENTRÉE: Nom d'utilisateur
        SORTIE: Liste des utilisateurs correspondant au nom d'utilisateur entré'''
    def fetch_client(self, username):
        self.cursor.execute("SELECT * FROM utilisateurs WHERE ut_username = %s", (username,))
        clients = self.cursor.fetchall()
        return clients

    ''' Cette fonction permet l'obtention de la liste des conducteurs.
        ENTREE : Nom d'utilisateur.
        SORTIE : Liste des conducteurs dont le nom correspond à celui entré en paramètre.'''
    def fetch_conducteur(self, username):
        self.cursor.execute("SELECT * FROM conducteur WHERE username = %s", (username,))
        conducteurs = self.cursor.fetchall()
        self.connection.close()
        return conducteurs

    ''' Cette fonction permet l'obtention de la liste des admins.
        ENTREE : Nom d'utilisateur.
        SORTIE : Liste des admins dont le nom correspond à celui entré en paramètre.'''
    def fetch_admin(self, username):
        self.cursor.execute("SELECT * FROM admins WHERE adm_username = %s", (username,))
        admins = self.cursor.fetchall()
        return admins

    ''' Cette fonction permet le rajout d'un nouveau voyage.
    ENTREE : Le lieu de départ du voyage, sa destination, le jour, l'heure ainsi que le prix.
    SORTIE : Rien'''
    def insert_voyage(self, departure, destination, days, hour, price):
        self.cursor.callproc("InsertVoyage", (departure, destination, price, hour, days))
        self.connection.close()

    ''' Cette fonction permet le rajout d'un voyage pour un utilisateur.
    ENTREE : L'ID du client et le numéro d'identification du voyage.
    SORTIE : Rien.'''
    def insert_new_voyage_utilisateur(self, vo_ni, id_utilisateur):
        self.cursor.execute(f"INSERT INTO voyage_utilisateur (vo_ni, id_utilisateur) VALUES "
                            f"('{vo_ni}', '{id_utilisateur}')")
        self.connection.close()

    ''' Cette fonction permet d'obtenir la liste des voyages d'un utilisateur.
    ENTREE : L'ID du client.
    SORTIE : Les informations complètes concernant les voyages d'un utilisateur.'''
    def get_voyages_user(self, id_utilisateur):
        self.cursor.execute(f"SELECT v.vo_ni, v.vo_dep, v.vo_dest, v.vo_heure_dep, v.vo_prix_passager "
                            f"FROM voyage_utilisateur vu JOIN voyage v ON vu.vo_ni = v.vo_ni "
                            f"WHERE vu.id_utilisateur = '{id_utilisateur}'")
        voyages = self.cursor.fetchall()
        self.connection.close()

        return [{"vo_ni": vo_ni, "vo_dep": vo_dep, "vo_dest": vo_dest,
                 "vo_heure_dep": vo_heure_dep, "vo_prix_passager": vo_prix_passager}
                for vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager in voyages]

    ''' Cette fonction permet de supprimer des voyages d'un utilisateur.
        ENTREE : L'ID du client et le numéro d'identification du voyage à supprimer.
        SORTIE : Rien.'''
    def delete_voyage_user(self, id_utilisateur, vo_ni):
        self.cursor.execute(f"DELETE FROM voyage_utilisateur "
                            f"WHERE id_utilisateur = '{id_utilisateur}' AND vo_ni = '{vo_ni}'")
        self.connection.close()

    ''' Cette fonction permet d'assigner une heure de travail à un conducteur.
        ENTREE : L'ID du conducteur et la date du voyage.
        SORTIE : Les informations complètes concernant le voyage assigné au conducteur.'''
    def fetch_horaire_conducteur(self, id_conducteur, date):
        self.cursor.execute(f"SELECT heure_debut, heure_fin, conger FROM horaire_conducteur "
                            f" WHERE id_conducteur = '{id_conducteur}' AND date = DATE('{date}') AND conger !=TRUE")
        result = self.cursor.fetchall()
        if len(result) == 0:
            return result
        self.connection.close()
        return [{"heure_debut": str(heure_debut), "heure_fin": str(heure_fin), "conger": conger}
                for heure_debut, heure_fin, conger in result]

    ''' Cette fonction permet de donner un jour de congé à un conducteur.
    ENTREE : L'ID du conducteur et la date du congé.
    SORTIE : Rien.'''
    def insert_day_off(self, id_conducteur, date):
        self.cursor.execute(f"SELECT voyage_av_midi, voyage_ap_midi, conger FROM horaire_conducteur "
                            f"WHERE id_conducteur = '{id_conducteur}' "
                            f"AND date = DATE('{date}')")
        conducteur_occupe = self.cursor.fetchone()
        if conducteur_occupe[2] == 1:
            raise ValueError("L'utilisateur est deja en conger")

        new_conducteurs_id = []
        if conducteur_occupe[0] == 1 or conducteur_occupe[1] == 1:
            self.cursor.execute(f"SELECT vo_ni FROM voyage "
                                f"WHERE id_conducteur = '{id_conducteur}' "
                                f"AND date = DATE('{date}')")
            voyages_trouves = self.cursor.fetchall()
            for voyage_id in voyages_trouves:
                try:
                    self.cursor.callproc("DemandeDeConger", (voyage_id, id_conducteur))
                    returned_id = self.cursor.fetchone()
                    new_conducteurs_id.append(returned_id[0])
                except Exception:
                    raise Exception("Ceci est une autre type d'erreur")

            if len(new_conducteurs_id) == len(voyages_trouves):
                try:
                    self.prise_de_conge(id_conducteur)
                    self.accepted_conger(id_conducteur, date)
                    self.new_conducteur_voyage(voyages_trouves, new_conducteurs_id)
                except Exception:
                    raise Exception("Ceci est une autre type d'erreur")
        else:
            try:
                self.prise_de_conge(id_conducteur)
            except Exception as e:
                raise Exception(f"Ceci est une autre type d'erreur : %s", e)

            try:
                self.accepted_conger(id_conducteur, date)
            except Exception as e:
                raise Exception(f"Ceci est une autre type d'erreur : %s", e)

    ''' Cette fonction permet d'assigner une nouvelle heure de travail à un conducteur.
    ENTREE : L'ID du conducteur et le voyage.
    SORTIE : Rien.'''
    def new_conducteur_voyage(self, voyages, new_conducteurs_id):
        numero_utilisateur = 0
        for voyage_id in voyages:
            self.cursor.execute(
                f"UPDATE voyage SET id_conducteur = '{new_conducteurs_id[numero_utilisateur]}' WHERE vo_ni = '{voyage_id}';")
            numero_utilisateur += 1

    ''' Cette fonction permet de valider le congé d'un conducteur.
        ENTREE : L'ID du conducteur et la date du congé.
        SORTIE : Rien.'''
    def accepted_conger(self, id_conducteur, date):
        self.cursor.execute(f"UPDATE horaire_conducteur "
                            f"SET conger = TRUE, voyage_av_midi = FALSE, voyage_ap_midi = FALSE "
                            f"WHERE id_conducteur = '{id_conducteur}' "
                            f"AND date = DATE('{date}')")

    ''' Cette fonction permet la gestion des congés d'un conducteur.
        ENTREE : L'ID du conducteur.
        SORTIE : Rien.'''
    def prise_de_conge(self, id_conducteur):
        self.cursor.execute(f"SELECT nb_jour_conger FROM conducteur WHERE id_conducteur = '{id_conducteur}'")
        nb_jours = self.cursor.fetchone()
        if nb_jours[0] > 0:
            self.cursor.execute(f"UPDATE conducteur SET nb_jour_conger = '{nb_jours[0] - 1}'"
                                f"WHERE id_conducteur = '{id_conducteur}'")
        else:
            raise TypeError("L'utilisateur n'a plus de jour de conger")

    ''' Cette fonction permet d'obtenir les voyages d'un conducteur à une date précise.
        ENTREE : L'ID du conducteur et la date.
        SORTIE : Liste contenant les informations complètes des voyage assignés à un conducteur à une daete précise.'''
    def get_voyages_conducteur(self, id_conducteur, date):
        heure_min = datetime.strptime(date, "%Y-%m-%d")
        heure_max = heure_min + timedelta(days=1)
        self.cursor.execute(f"SELECT vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager "
                            f"FROM voyage "
                            f"WHERE id_conducteur = '{id_conducteur}' "
                            f"AND vo_heure_dep BETWEEN '{heure_min.date()}' AND '{heure_max.date()}' "
                            f"ORDER BY vo_heure_dep")
        result = self.cursor.fetchall()
        self.connection.close()
        return [
            {"vo_ni": vo_ni, "depart": vo_dep, "destination": vo_dest, "date_temps": vo_heure_dep,
             "prix": vo_prix_passager}
            for vo_ni, vo_dep, vo_dest, vo_heure_dep, vo_prix_passager in result]
