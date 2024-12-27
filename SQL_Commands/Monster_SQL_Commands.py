import sys
from typing import List

from utils import general_utils
from utils.Logger import MyLogger as logger
from Connectors.dbConnector import monster_battler_db_connector as db_con
from random import randint

connection = db_con()


def does_monster_exist(monster_id: str):
    jsonArray = get_monster(monster_id=monster_id)
    if len(jsonArray) == 0:
        return False
    return True


def create_monster(monster_id: str, monster_species_id: str, monster_name: str = None, monster_species_form: int = 1):
    this_name = f"\'{monster_name}\'"
    sql = (
        f"insert into monsters (monster_id, monster_species_id, monster_species_form"
        f"{', monster_name' if monster_name is not None else ''}) "
        f"values('{monster_id}', '{monster_species_id}', {monster_species_form}{f', {this_name}'});")
    connection.insertCall(sql)

    sql = f"insert into monster_stats (monster_id) values('{monster_id}')"
    connection.insertCall(sql)

    sql = (f"insert into monster_IVs (monster_id, hp, pAttk, pDef, sAttk, sDef, spd) values('{monster_id}', "
           f"{randint(0,31)}, {randint(0,31)},{randint(0,31)},{randint(0,31)},"
           f"{randint(0,31)},{randint(0,31)})")
    connection.insertCall(sql)

    sql = f"insert into monster_EVs (monster_id) values('{monster_id}')"
    connection.insertCall(sql)


def get_monster(monster_id: str):
    sql = f"select * from monsters where monster_id = '{monster_id}' and archived = false;"
    return connection.selectCall(sql)


def update_monster_name(monster_id: str, monster_name):
    sql = f"update monsters set monster_name = '{monster_name}' where monster_id = '{monster_id}' and archived = false;"
    return connection.insertCall(sql)


def update_monster_species(monster_id: str, monster_species_id: str, monster_species_form: int = 1):
    sql = (f"update monsters set monster_species_id = '{monster_species_id}', "
           f"monster_species_form = {monster_species_form} where monster_id = '{monster_id}' and archived = false;")
    return connection.insertCall(sql)


def archive_monster(monster_id: str):
    sql = f"update monsters set archived = true where monster_id = '{monster_id}' and archived = false;"
    return connection.insertCall(sql)


def restore_monster(monster_id: str):
    sql = f"update monsters set archived = false where monster_id = '{monster_id}' and archived = true;"
    return connection.insertCall(sql)


def get_monster_ivs(monster_id: str):
    sql = f"select * from monster_IVs where monster_id = '{monster_id}' and archived = false;"
    return connection.selectCall(sql)


def get_monster_evs(monster_id: str):
    sql = f"select * from monster_EVs where monster_id = '{monster_id}' and archived = false;"
    return connection.selectCall(sql)

def get_monster_stats(monster_id: str):
    sql = f"select * from monster_stats where monster_id = '{monster_id}' and archived = false;"
    return connection.selectCall(sql)
def get_monster_species(monster_species_id: str, monster_species_form: int = 1):
    sql = (f"select * from monsters_species where monster_species_id = '{monster_species_id}' and "
           f"monster_species_form = {monster_species_form} and archived = false;")
    return connection.selectCall(sql)

def get_monster_species_base_stats(monster_species_id: str, monster_species_form: int = 1):
    sql = (f"select * from monster_species_base_stats where monster_species_id = '{monster_species_id}' and "
           f"monster_species_form = {monster_species_form} and archived = false;")
    return connection.selectCall(sql)
