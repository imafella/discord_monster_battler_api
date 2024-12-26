# Class for connecting to database.
# with a simple API that has no logic other than retrieving and posting to a database

import json
import os

import mysql.connector


class monster_battler_db_connector:
    def __init__(self):
        self.db_host = os.environ.get('db_host', None)
        self.db_name = os.environ.get('db_name', None)
        self.db_username = os.environ.get("db_user", None)
        self.db_password = os.environ.get("db_password", None)
        self.dbConnection = None
        self.cursor = None
        self.connectToDB()
        self.cursor.close()
        self.dbConnection.close()

    # Sets up the config

    def connectToDB(self):
        self.dbConnection = mysql.connector.connect(user=self.db_username, password=self.db_password, host=self.db_host,
                                                    database=self.db_name
                                                    )
        self.cursor = self.dbConnection.cursor(buffered=True)

    def closeConnectionToDB(self):
        self.cursor.close()
        self.dbConnection.close()

    def selectCall(self, sql):
        self.connectToDB()
        self.cursor.execute(sql)
        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        result = [dict(zip(column_names, row))
                  for row in self.cursor.fetchall()]
        self.closeConnectionToDB()
        return result

    def insertCall(self, sql):
        self.connectToDB()
        self.cursor.execute(sql)
        lastId = self.cursor.lastrowid
        self.dbConnection.commit()
        self.closeConnectionToDB()
        return lastId
