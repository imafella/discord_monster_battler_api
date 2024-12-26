import json
import sys
from datetime import datetime
import logging
from typing import List

sys.path.append('..utils')
from utils import general_utils
from utils.Logger import MyLogger as logger

sys.path.append('..Models')
from Models.Monster_Models import Monster


def get_monster_index(monster_id: str, monster_list: List[Monster]):
    for index, monster in enumerate(monster_list):
        if monster_id is monster.monster_id:
            return index
    return None


class Tamer:
    def __init__(self, discord_id: str = None):
        self.tamer_id = discord_id
        self.tamer_party = []
        self.tamer_monster_storage = []
        self.active_battle_id = None
        self.logger = logger()
        output = {
            "class": "Tamer_Models",
            "Method": "__init__",
            "tamer_id": self.tamer_id,
            "monsters_in_party": len(self.tamer_party),
            "monsters_in_tamer_monster_storage": len(self.tamer_monster_storage),
            "message": f"Initialized Tamer: {self.tamer_id}"
        }
        self.logger.log(message=output)

    def from_json(self, tamer_json: dict):
        self.tamer_id = tamer_json.get('tamer_id', None)
        self.tamer_party = json.loads(tamer_json.get('tamer_party', "[]"))
        self.tamer_monster_storage = json.loads(tamer_json.get('tamer_monster_storage', "[]"))
        self.active_battle_id = tamer_json.get('active_battle_id', None)
        output = {
            "class": "Tamer_Models",
            "Method": "from_json",
            "tamer_id": self.tamer_id,
            "monsters_in_party": len(self.tamer_party),
            "monsters_in_tamer_monster_storage": len(self.tamer_monster_storage),
            "message": f"Loaded Tamer: {self.tamer_id}"
        }
        self.logger.log(message=output)


    def add_monster_to_party(self, new_monster: Monster):
        if len(self.tamer_party) > 5:
            output = {
                "class": "Tamer_Models",
                "Method": "add_monster_to_party",
                "tamer_id": self.tamer_id,
                "monster_id": new_monster.monster_id,
                "monsters_in_party": len(self.tamer_party),
                "tamer_party": json.dumps(general_utils.obj_to_dict(self.tamer_party)),
                "message": f"Too many monsters in party to add to party."
            }
            self.logger.log(message=output)
            output = self.add_monster_to_tamer_monster_storage(new_monster)
            return output
        self.tamer_party.append(new_monster)
        output = {
            "class": "Tamer_Models",
            "Method": "add_monster_to_party",
            "tamer_id": self.tamer_id,
            "monster_id": new_monster.monster_id,
            "monsters_in_party": len(self.tamer_party),
            "message": f"Added {new_monster.monster_name} to party."
        }
        self.logger.log(message=output)
        return output

    def add_monster_to_tamer_monster_storage(self, new_monster_for_tamer_monster_storage: Monster):
        if len(self.tamer_monster_storage) > 19:
            output = {
                "class": "Tamer_Models",
                "Method": "add_monster_to_tamer_monster_storage",
                "tamer_id": self.tamer_id,
                "new_monster_for_tamer_monster_storage": json.dumps(general_utils.obj_to_dict(
                    new_monster_for_tamer_monster_storage)),
                "monsters_in_tamer_monster_storage": len(self.tamer_monster_storage),
                "error": "Too many monsters in tamer_monster_storage to add to tamer monster storage. "
                         "Please resolve this.",
                "error_code": 405
            }
            self.logger.log(message=output)
            return output
        self.tamer_monster_storage.append(new_monster_for_tamer_monster_storage)
        output = {
            "class": "Tamer_Models",
            "Method": "add_monster_to_tamer_monster_storage",
            "tamer_id": self.tamer_id,
            "monsters_in_tamer_monster_storage": len(self.tamer_monster_storage),
            "message": f"Added {new_monster_for_tamer_monster_storage.monster_name} to tamer_monster_storage."
        }
        self.logger.log(message=output)
        return output

    def move_monster_to_tamer_monster_storage_from_party(self, monster_id):
        index = get_monster_index(monster_id=monster_id, monster_list=self.tamer_party)
        if index is None:
            output = {
                "class": "Tamer_Models",
                "Method": "move_monster_to_tamer_monster_storage_from_party",
                "tamer_id": self.tamer_id,
                "monster_id": monster_id,
                "message": f"Monster: {monster_id} is not in the tamer_monster_storage."
            }
            self.logger.log(message=output)
            return output
        selected_monster = self.tamer_party.pop(index)
        return self.add_monster_to_tamer_monster_storage(new_monster_for_tamer_monster_storage=selected_monster)

    def move_monster_to_party_from_tamer_monster_storage(self, monster_id):
        index = get_monster_index(monster_id=monster_id, monster_list=self.tamer_monster_storage)
        if index is None:
            output = {
                "class": "Tamer_Models",
                "Method": "move_monster_to_party_from_tamer_monster_storage",
                "tamer_id": self.tamer_id,
                "monster_id": monster_id,
                "message": f"Monster: {monster_id} is not in the tamer_party."
            }
            self.logger.log(message=output)
            return output
        selected_monster = self.tamer_monster_storage.pop(index)
        return self.add_monster_to_party(new_monster=selected_monster)

    def remove_monster(self,monster_id):
        index_party = get_monster_index(monster_id=monster_id, monster_list=self.tamer_party)
        index_tamer_monster_storage = None
        if index_party is None:
            index_tamer_monster_storage = get_monster_index(monster_id=monster_id, monster_list=self.tamer_monster_storage)
            if index_tamer_monster_storage is None:
                output = {
                    "class": "Tamer_Models",
                    "Method": "remove_monster",
                    "tamer_id": self.tamer_id,
                    "monster_id": monster_id,
                    "error": f"Monster: {monster_id} is not owned by the tamer.",
                    "error_code": 404
                }
            else:
                removed_monster = self.tamer_monster_storage.pop(index_tamer_monster_storage)
                output = {
                    "class": "Tamer_Models",
                    "Method": "remove_monster",
                    "tamer_id": self.tamer_id,
                    "monster_id": monster_id,
                    "message": f"Monster: {removed_monster.monster_name} has been removed from the "
                               f"tamer_monster_storage."
                }
        else:
            removed_monster = self.tamer_party.pop(index_party)
            output = {
                "class": "Tamer_Models",
                "Method": "remove_monster",
                "tamer_id": self.tamer_id,
                "monster_id": monster_id,
                "message": f"Monster: {removed_monster.monster_name} has been removed from the "
                           f"tamer_party."
            }

        self.logger.log(message=output)
        return output

    #TODO check if battle_id is an active battle
    def start_battle(self, battle_id):
        output ={
            "class": "Tamer_Models",
            "Method": "start_battle",
            "tamer_id": self.tamer_id,
            "new_active_battle_id": battle_id,
            "message": f"{self.tamer_id} is added to the battle: {battle_id}"
        }
        self.logger.log(message=output)
        self.active_battle_id = battle_id
        return output

    def end_battle(self):
        if self.active_battle_id is not None:
            output = {
                "class": "Tamer_Models",
                "Method": "start_battle",
                "tamer_id": self.tamer_id,
                "new_active_battle_id": self.active_battle_id,
                "message": f"Battle: {self.active_battle_id} has finished. {self.tamer_id} is no longer in battle"
            }
            self.logger.log(message=output)
        else:
            output = {
                "class": "Tamer_Models",
                "Method": "start_battle",
                "tamer_id": self.tamer_id,
                "new_active_battle_id": self.active_battle_id,
                "error": f"{self.tamer_id} is not in an active battle.",
                "error_code": 405
            }
        self.active_battle_id = None
        return output

    def get_party_list(self):
        party_list = []
        for monster in self.tamer_party:
            party_list.append(monster.monster_id)
        return party_list

    def get_tamer_monster_storage_list(self):
        tamer_monster_storage_list = []
        for monster in self.tamer_monster_storage:
            tamer_monster_storage_list.append(monster.monster_id)
        return tamer_monster_storage_list
