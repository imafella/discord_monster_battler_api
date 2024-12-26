import sys

sys.path.append('..utils')
from utils import general_utils
from utils.Logger import MyLogger as logger

sys.path.append('..Connectors')
from Connectors.dbConnector import monster_battler_db_connector as db_con

connection = db_con()


def create_database(db_name: str):
    sql = f"create database if not exists {db_name};"
    return connection.insertCall(sql)


def create_tamer_table():
    sql = ("create table if not exists monster_battler.tamers (tamer_id varchar(255) not null primary key, "
           + "active_battle_id varchar(255) default null,tamer_party text, tamer_monster_storage text, "
           + "archived bool not null default False);")
    return connection.insertCall(sql)
