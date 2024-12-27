from typing import List

from Models.Monster_Models import Monster
from SQL_Commands import Monster_SQL_Commands
from utils.Logger import MyLogger as Logger

logger = Logger()

def load_monsters(monsters: List[str]):
    monster_list = []
    for monster_id in monsters:
        monster = load_monster(monster_id=monster_id)
        if monster.monster_species_id is "":
            continue
        monster_list.append(monster)
    return monster_list


def load_monster(monster_id: str) -> Monster:
    if Monster_SQL_Commands.does_monster_exist(monster_id=monster_id):
        monster_json = Monster_SQL_Commands.get_monster(monster_id=monster_id)[0]
        monster_ivs_json = Monster_SQL_Commands.get_monster_ivs(monster_id=monster_id)[0]
        monster_evs_json = Monster_SQL_Commands.get_monster_evs(monster_id=monster_id)[0]
        monster_species_base_stats_json = (
            Monster_SQL_Commands.get_monster_species_base_stats(
                monster_species_id=monster_json.get('monster_species_id', 0),
                monster_species_form=monster_json.get("monster_species_form", 1)
            )[0]
        )
        monster_json['monster_ivs'] = monster_ivs_json
        monster_json['monster_evs'] = monster_evs_json
        monster_json['monster_species_base_stats'] = monster_species_base_stats_json
        monster = Monster("")
        monster.from_json(monster_json=monster_json)
        return monster
    logger.log(message={
        "class":"InfoLoader",
        "method":"load_monster",
        "monster_id": monster_id,
        "error":f"Monster: {monster_id} does not exist",
        "error_code":404
    })
    return Monster("")
