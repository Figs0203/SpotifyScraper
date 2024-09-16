"""
import typing
import mysql.connector as mariadb  # Renombrar para evitar confusión con SpotifyScraper
from dotenv import load_dotenv
import os

load_dotenv()

if typing.TYPE_CHECKING:
    from Song import Song

class SongService:
    def __init__(self):
        # Cargar variables de entorno
        self.tableName = os.getenv("DB_TABLE_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_name = os.getenv("DB_NAME")

        # Verificar si las variables de entorno están definidas
        if not all([self.tableName, db_user, db_pass, db_name]):
            raise ValueError("Error: Algunas variables de entorno no están definidas.")
        
        # Conectar a la base de datos
        self.connection = mariadb.connect(
            user=db_user,
            password=db_pass,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def save(self, song: 'Song'):
        self.cursor.execute(
            "INSERT INTO {} (name, artist, ranking, country, date) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE "
            "name=VALUES(name), "
            "artist=VALUES(artist), "
            "ranking=VALUES(ranking), "
            "country=VALUES(country), "
            "date=VALUES(date)".format(self.tableName),
            (song.name, song.author, song.ranking, song.country, song.date)
        )
        self.connection.commit()
"""

import typing
import mysql.connector as SpotifyDB  # Renombrar para evitar confusión con SpotifyScraper

if typing.TYPE_CHECKING:
    from Song import Song

class SongService:
    def __init__(self):
        # Cargar variables de entorno
        self.tableName = ("Name")
        db_user = ("User")
        db_pass = ("Password")
        db_name = ("DB_name")

        # Verificar si las variables de entorno están definidas
        if not all([self.tableName, db_user, db_pass, db_name]):
            raise ValueError("Error: Algunas variables de entorno no están definidas.")
        
        # Conectar a la base de datos
        self.connection = SpotifyDB.connect(
            user=db_user,
            password=db_pass,
            database=db_name
        )
        self.cursor = self.connection.cursor()

    def save(self, song: 'Song'):
        self.cursor.execute(
            "INSERT INTO {} (name, artist, ranking, country, date) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE "
            "name=VALUES(name), "
            "artist=VALUES(artist), "
            "ranking=VALUES(ranking), "
            "country=VALUES(country), "
            "date=VALUES(date)".format(self.tableName),
            (song.name, song.author, song.ranking, song.country, song.date)
        )
        self.connection.commit()