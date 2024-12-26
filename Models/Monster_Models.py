import sys
from datetime import datetime
import logging

sys.path.append('..utils')
from utils import general_utils

logging.basicConfig(
    filename=f"{datetime.now().strftime('%Y-%m-%d')}_monster.log",
    format='%(asctime)s %(message)s',
    filemode='w'
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Monster:
    def __init__(self, species_id, monster_name: str = None):
        self.monster_id = general_utils.generate_id("Mon")
        self.monster_species_id = species_id
        self.monster_name = monster_name
        self.monster_stats = MonsterStats()


class MonsterStats:
    def __init__(self):
        self.hp = 0
        self.pAttk = 0
        self.pDef = 0
        self.sAttk = 0
        self.sDef = 0
        self.spd = 0
