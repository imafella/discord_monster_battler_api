import json
import sys
from datetime import datetime
import logging
from math import floor

from utils import general_utils
from utils.Logger import MyLogger as Logger


class Monster:
    def __init__(self, species_id: str, monster_name: str = None):
        self.monster_id = general_utils.generate_id("Mon")
        self.monster_species_id = species_id
        self.monster_species_form = 1
        self.monster_species_name = None
        self.monster_name = monster_name
        self.monster_nature = MonsterNature()
        self.level = 1
        self.exp_total = 0
        self.monster_ivs = MonsterIVs()
        self.monster_evs = MonsterEVs()
        self.monster_species_base_stats = MonsterSpeciesBaseStats()
        self.monster_stats = MonsterStats()
        self.logger = Logger()

    def from_json(self, monster_json: dict):
        self.monster_id = monster_json.get('monster_id', None)
        self.monster_species_id = monster_json.get('monster_species_id', None)
        self.monster_species_form = monster_json.get('monster_species_form', 1)
        self.monster_species_name = monster_json.get('monster_species_name', None)
        self.monster_name = monster_json.get('monster_name', None)
        self.monster_nature.from_json(nature_json=monster_json.get('monster_nature', {}), monster_id=self.monster_id)
        self.monster_ivs.from_json(ivs_json=monster_json.get('monster_ivs', {}),
                                   monster_id=self.monster_id)
        self.monster_evs.from_json(evs_json=monster_json.get('monster_evs', {}),
                                   monster_id=self.monster_id)
        self.monster_species_base_stats.from_json(monsterStats_json=monster_json.get('monster_species_base_stats', {}),
                                                  monster_id=self.monster_id)
        self.generate_current_stats()
        self.level = monster_json.get("level", 1)
        self.exp_total = monster_json.get("exp_total", 0)
        output = {
            "class": "Monster_Models",
            "Method": "from_json",
            "monster_id": self.monster_id,
            "monster_species_id": self.monster_species_id,
            "monster_name": self.monster_name,
            "message": f"Loaded Monster: {self.monster_id}"
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"monster_id": self.monster_id, "monster_species_id": self.monster_species_id,
                "monster_species_form": self.monster_species_form, "monster_name": self.monster_name,
                "monster_stats": self.monster_stats.to_dict(), "level": self.level, "exp_total": self.exp_total,
                "nature": self.monster_nature.to_dict(), "monster_species_name":self.monster_species_name}

    def generate_current_stats(self):
        """
        From the game!
        HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
        Other Stats = (floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature
        """
        self.monster_stats.hp = 10 + self.level + floor(
            (0.01 * (2 * self.monster_species_base_stats.hp + self.monster_ivs.hp +
                     floor(0.25 * self.monster_evs.hp) * self.level)))

        nature_mod = self.monster_nature.get_nature_mod('pAttk')
        self.monster_stats.pAttk = nature_mod * (
                floor(0.01 * (2 * self.monster_species_base_stats.pAttk + self.monster_ivs.pAttk +
                              floor(0.25 * self.monster_evs.pAttk)) * self.level) + 5
        )

        nature_mod = self.monster_nature.get_nature_mod('pDef')
        self.monster_stats.pDef = nature_mod * (
                floor(0.01 * (2 * self.monster_species_base_stats.pDef + self.monster_ivs.pDef +
                              floor(0.25 * self.monster_evs.pDef)) * self.level) + 5
        )

        nature_mod = self.monster_nature.get_nature_mod('sAttk')
        self.monster_stats.sAttk = nature_mod * (
                floor(0.01 * (2 * self.monster_species_base_stats.sAttk + self.monster_ivs.sAttk +
                              floor(0.25 * self.monster_evs.sAttk)) * self.level) + 5
        )

        nature_mod = self.monster_nature.get_nature_mod('sDef')
        self.monster_stats.sDef = nature_mod * (
                floor(0.01 * (2 * self.monster_species_base_stats.sDef + self.monster_ivs.sDef +
                              floor(0.25 * self.monster_evs.sDef)) * self.level) + 5
        )

        nature_mod = self.monster_nature.get_nature_mod('spd')
        self.monster_stats.spd = nature_mod * (
                floor(0.01 * (2 * self.monster_species_base_stats.spd + self.monster_ivs.spd +
                              floor(0.25 * self.monster_evs.spd)) * self.level) + 5
        )


class MonsterSpecies:
    def __init__(self, monster_species_id: str, monster_species_form: int = 1):
        self.monster_species_id = monster_species_id
        self.monster_species_form = monster_species_id
        self.monster_species_name = None
        self.logger = Logger()

    def from_json(self, monster_species_json: dict):
        self.monster_species_id = monster_species_json.get('monster_species_id', None)
        self.monster_species_form = monster_species_json.get('monster_species_form', 1)
        self.monster_species_name = monster_species_json.get('monster_species_name', None)
        output = {
            "class": "MonsterSpecies",
            "Method": "from_json",
            "monster__species_id": self.monster_species_id,
            "monster_species_form": self.monster_species_form,
            "monster_species_name": self.monster_species_name,
            "message": f"Loaded Monster Species: {self.monster_species_name}"
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"monster_species_id": self.monster_species_id, "monster_species_form": self.monster_species_form,
                "monster_species_name": self.monster_species_name}


class MonsterStats:
    def __init__(self):
        self.hp = 0
        self.pAttk = 0
        self.pDef = 0
        self.sAttk = 0
        self.sDef = 0
        self.spd = 0
        self.logger = Logger()

    def from_json(self, monsterStats_json: dict, monster_id):
        self.hp = monsterStats_json.get('hp', 0)
        self.pAttk = monsterStats_json.get('pAttk', 0)
        self.pDef = monsterStats_json.get('pDef', 0)
        self.sAttk = monsterStats_json.get('sAttk', 0)
        self.sDef = monsterStats_json.get('sDef', 0)
        self.spd = monsterStats_json.get('spd', 0)
        output = {
            "class": "MonsterStats",
            "Method": "from_json",
            "monster_id": monster_id,
            "stats": json.dumps(self.to_dict())
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"hp": self.hp, "pAttk": self.pAttk, "pDef": self.pDef, "sAttk": self.sAttk, "sDef": self.sDef,
                "spd": self.spd}


class MonsterEVs:
    def __init__(self):
        self.hp = 0
        self.pAttk = 0
        self.pDef = 0
        self.sAttk = 0
        self.sDef = 0
        self.spd = 0
        self.logger = Logger()

    def from_json(self, evs_json: dict, monster_id):
        self.hp = evs_json.get('hp', 0)
        self.pAttk = evs_json.get('pAttk', 0)
        self.pDef = evs_json.get('pDef', 0)
        self.sAttk = evs_json.get('sAttk', 0)
        self.sDef = evs_json.get('sDef', 0)
        self.spd = evs_json.get('spd', 0)
        output = {
            "class": "MonsterEVs",
            "Method": "from_json",
            "monster_id": monster_id,
            "stats": json.dumps(self.to_dict())
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"hp": self.hp, "pAttk": self.pAttk, "pDef": self.pDef, "sAttk": self.sAttk, "sDef": self.sDef,
                "spd": self.spd}


class MonsterIVs:
    def __init__(self):
        self.hp = 0
        self.pAttk = 0
        self.pDef = 0
        self.sAttk = 0
        self.sDef = 0
        self.spd = 0
        self.logger = Logger()

    def from_json(self, ivs_json: dict, monster_id):
        self.hp = ivs_json.get('hp', 0)
        self.pAttk = ivs_json.get('pAttk', 0)
        self.pDef = ivs_json.get('pDef', 0)
        self.sAttk = ivs_json.get('sAttk', 0)
        self.sDef = ivs_json.get('sDef', 0)
        self.spd = ivs_json.get('spd', 0)
        output = {
            "class": "MonsterIVs",
            "Method": "from_json",
            "monster_id": monster_id,
            "stats": json.dumps(self.to_dict())
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"hp": self.hp, "pAttk": self.pAttk, "pDef": self.pDef, "sAttk": self.sAttk, "sDef": self.sDef,
                "spd": self.spd}


class MonsterSpeciesBaseStats:
    def __init__(self):
        self.hp = 0
        self.pAttk = 0
        self.pDef = 0
        self.sAttk = 0
        self.sDef = 0
        self.spd = 0
        self.logger = Logger()

    def from_json(self, monsterStats_json: dict, monster_id):
        self.hp = monsterStats_json.get('hp', 0)
        self.pAttk = monsterStats_json.get('pAttk', 0)
        self.pDef = monsterStats_json.get('pDef', 0)
        self.sAttk = monsterStats_json.get('sAttk', 0)
        self.sDef = monsterStats_json.get('sDef', 0)
        self.spd = monsterStats_json.get('spd', 0)
        output = {
            "class": "MonsterSpeciesBaseStats",
            "Method": "from_json",
            "monster_id": monster_id,
            "stats": json.dumps(self.to_dict())
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"hp": self.hp, "pAttk": self.pAttk, "pDef": self.pDef, "sAttk": self.sAttk, "sDef": self.sDef,
                "spd": self.spd}


class MonsterNature:
    def __init__(self):
        self.nature_id = None
        self.nature_name = None
        self.nature_boon = None
        self.nature_bane = None
        self.logger = Logger()

    def from_json(self, nature_json: dict, monster_id):
        self.nature_id = nature_json.get('nature_id', None)
        self.nature_name = nature_json.get('nature_name', None)
        self.nature_bane = nature_json.get('nature_bane', None)
        self.nature_boon = nature_json.get('nature_boon', None)
        output = {
            "class": "MonsterSpeciesBaseStats",
            "Method": "from_json",
            "monster_id": monster_id,
            "Nature": json.dumps(self.to_dict())
        }
        self.logger.log(message=output)

    def to_dict(self):
        return {"nature_id": self.nature_id, "nature_name": self.nature_name, "nature_boon": self.nature_boon,
                "nature_bane": self.nature_bane}

    def get_nature_mod(self, stat: str):
        nature_mod = 1.0
        if self.nature_boon is stat:
            nature_mod += 0.1
        if self.nature_bane is stat:
            nature_mod -= 0.1
        return nature_mod
