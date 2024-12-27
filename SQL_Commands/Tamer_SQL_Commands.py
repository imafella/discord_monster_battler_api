import sys
from typing import List

sys.path.append('..utils')
from utils import general_utils
from utils.Logger import MyLogger as logger
sys.path.append('..Connectors')
from Connectors.dbConnector import monster_battler_db_connector as db_con

connection = db_con()

def does_tamer_exist(discord_id: str):
    jsonArray = get_tamer(discord_id=discord_id)
    if len(jsonArray) == 0:
        return False
    return True
def insert_tamer(discord_id:str):
    sql = f"insert into tamers (tamer_id, tamer_party, tamer_monster_storage) values('{discord_id}', '[]', '[]');"
    return connection.insertCall(sql)
def get_tamer(discord_id:str):
    sql = f"select * from tamers where tamer_id = '{discord_id}';"
    return connection.selectCall(sql)

def get_tamers():
    sql = f"select * from tamers where archived = false;"
    return connection.selectCall(sql)

def update_tamer_party(discord_id:str, tamer_party: List[str]):
    sql = f"update tamers set tamer_party = '{tamer_party}' where tamer_id = '{discord_id}' and archived = false;"
    return connection.insertCall(sql)

def update_tamer_monster_storage(discord_id:str, tamer_monster_storage: List[str]):
    sql = f"update tamers set tamer_monster_storage = '{tamer_monster_storage}' where tamer_id = '{discord_id}' and archived = false;"
    return connection.insertCall(sql)

def archive_tamer(discord_id:str):
    sql = f"update tamers set archived = true where tamer_id = '{discord_id}' and archived = false;"
    return connection.insertCall(sql)

def restore_tamer(discord_id:str):
    sql = f"update tamers set archived = false where tamer_id = '{discord_id}' and archived = true;"
    return connection.insertCall(sql)

def update_battle_status(discord_id:str, battle_id:str = 'null'):
    """
    Can be used to either give a tamer an active battle or clear it.
    """
    if battle_id != 'null':
        battle_id = "\'"+battle_id+"\'"
    sql = f"update tamers set active_battle_id = {battle_id} where tamer_id = '{discord_id}' and archived = false;"
    return connection.insertCall(sql)