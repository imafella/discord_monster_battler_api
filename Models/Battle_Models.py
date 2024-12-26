import sys
from datetime import datetime
sys.path.append('..utils')
from utils import general_utils


class Battle:
    def __init__(self, battle_id: str = None, initiating_id: str = None, target_id: str = None):
        self.initiating_tamer_id = initiating_id
        self.target_id = target_id
        if battle_id is None:
            battle_id = general_utils.generate_id("Bat")
        self.battle_id = battle_id
        self.is_active = True
