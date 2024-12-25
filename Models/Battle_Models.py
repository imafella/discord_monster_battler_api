from datetime import datetime


def generate_id():
    return datetime.now().strftime('B-%Y%m%d%H%M%S')


class Battle:
    def __init__(self, battle_id: str = None, initiating_id: str = None, target_id: str = None):
        self.initiating_tamer_id = initiating_id
        self.target_id = target_id
        if battle_id is None:
            battle_id = generate_id()
        self.battle_id = battle_id
        self.is_active = True

