import json
import logging
import os
import sys
from datetime import datetime

from flask import Blueprint
from flask import request, Response

from Models.Monster_Models import Monster
from Models.Tamer_Models import Tamer

from utils import general_utils, InfoLoader
from utils.Logger import MyLogger as Logger

sys.path.append('..SQL_Commands')
from SQL_Commands import Tamer_SQL_Commands, Monster_SQL_Commands

tamer_bp = Blueprint('tamer', __name__)
logger = Logger()


@tamer_bp.route('/tamer', methods=['POST'])
def post_tamer():
    api_request = request.json
    discord_id = api_request.get('discord_id', None)
    if discord_id is None:
        return general_utils.response_formatter({"error": "No discord_id provided", "error_code": 400}, 400)
    new_tamer = Tamer(discord_id=discord_id)
    Tamer_SQL_Commands.insert_tamer(discord_id=discord_id)
    if Tamer_SQL_Commands.does_tamer_exist(discord_id=discord_id):
        return general_utils.response_formatter(body={"Message": f"Tamer: {new_tamer.tamer_id} has been created.",
                                                      "tamer_id": new_tamer.tamer_id},
                                                status=201)
    else:
        return general_utils.response_formatter(body={"error": "Unable to insert", "error_code": 500}, status=500)


@tamer_bp.route('/tamer/<tamer_id>', methods=['GET'])
def get_tamer(tamer_id):
    if not Tamer_SQL_Commands.does_tamer_exist(discord_id=tamer_id):
        return general_utils.response_formatter({"error": "Tamer not found"}, 404)
    tamer_json = Tamer_SQL_Commands.get_tamer(discord_id=tamer_id)[0]
    tamer = Tamer()
    tamer.from_json(tamer_json)
    return general_utils.response_formatter(body=tamer.to_dict(), status=200)


@tamer_bp.route('/tamer', methods=['GET'])
def get_tamers():
    tamers_json = Tamer_SQL_Commands.get_tamers()
    logger.log(message={"tamers":tamers_json})
    tamers = []
    for tamer_json in tamers_json:
        tamer = Tamer()
        tamer.from_json(tamer_json)
        tamers.append(tamer)
    return general_utils.response_formatter(body={"tamers":[tamer.to_dict() for tamer in tamers], "number_of_tamers":len(tamers)}, status=200)


@tamer_bp.route('/tamer/<tamer_id>', methods=['DELETE'])
def archive_tamer(tamer_id):
    if not Tamer_SQL_Commands.does_tamer_exist(discord_id=tamer_id):
        return general_utils.response_formatter(body={"error": "Tamer not found"}, status=404)
    Tamer_SQL_Commands.archive_tamer(discord_id=tamer_id)

    tamer_json = Tamer_SQL_Commands.get_tamer(discord_id=tamer_id)[0]
    if tamer_json.get('archived', 0) is 0:
        return general_utils.response_formatter(body={"error": f"Unable to archive Tamer: {tamer_id}"},
                                                status=500)

    return general_utils.response_formatter(body=tamer_json, status=200)


@tamer_bp.route('/tamer/<tamer_id>', methods=['PATCH'])
def patch_tamer(tamer_id):
    """

    :body expected: {optional tamer_party [monster_ids] or tamer_monster_storage [monster_ids] or monster_id str}
    :return:
    """
    if not Tamer_SQL_Commands.does_tamer_exist(discord_id=tamer_id):
        return general_utils.response_formatter({"error": "Tamer not found"}, 404)
    tamer_json = Tamer_SQL_Commands.get_tamer(discord_id=tamer_id)[0]
    tamer = Tamer()
    tamer.from_json(tamer_json)
    tamer.tamer_party = InfoLoader.load_monsters(tamer.tamer_party)

    api_request = request.json
    # Assume this is a list of monster_ids
    tamer_party = api_request.get('tamer_party', [])
    # Assume this is a list of monster_ids
    tamer_monster_storage = api_request.get('tamer_monster_storage', [])
    active_battle_id = api_request.get('active_battle_id', None)
    monster_id = api_request.get('monster_id', None)

    msg = ""

    # Handles changing the battle status of the Tamer.
    if active_battle_id != tamer.active_battle_id:
        if active_battle_id is None:
            tamer_response = tamer.end_battle()
            if 'error' in tamer_response:
                return general_utils.response_formatter(body=tamer_response,
                                                        status=tamer_response.get('error_code', 500))
            Tamer_SQL_Commands.update_battle_status(discord_id=tamer.tamer_id)
            msg += " " + tamer_response.get('message', "")
        else:
            tamer_response = tamer.start_battle(battle_id=active_battle_id)
            if 'error' in tamer_response:
                return general_utils.response_formatter(body=tamer_response,
                                                        status=tamer_response.get('error_code', 500))
            Tamer_SQL_Commands.update_battle_status(discord_id=tamer.tamer_id, battle_id=tamer.active_battle_id)
            msg += " " + tamer_response.get('message', "")

    # Handles receiving/releasing a new monster
    if monster_id is not None:
        # TODO load full monster details from monster ID SQL call instead of the below
        party_index = tamer.get_monster_party_index(monster_id=monster_id)
        tamer_monster_storage_index = tamer.get_monster_tamer_monster_storage_index(monster_id=monster_id)

        # Handle removing monster.
        if party_index is not None or tamer_monster_storage_index is not None:
            tamer_response = tamer.remove_monster(monster_id=monster_id)
            if 'error' in tamer_response:
                return general_utils.response_formatter(body=tamer_response,
                                                        status=tamer_response.get('error_code', 500))
            msg += " " + tamer_response.get('message', "")
            Tamer_SQL_Commands.update_tamer_party(discord_id=tamer.tamer_id, tamer_party=tamer.get_party_list())
            Tamer_SQL_Commands.update_tamer_monster_storage(discord_id=tamer.tamer_id,
                                                            tamer_monster_storage=tamer.tamer_monster_storage)
        else:
            new_monster = InfoLoader.load_monster(monster_id)
            tamer_response = tamer.add_monster_to_party(new_monster=new_monster)
            if 'error' in tamer_response:
                return general_utils.response_formatter(body=tamer_response,
                                                        status=tamer_response.get('error_code', 500))
            if tamer_response.get('Method', None) is 'add_monster_to_party':
                monster_ids = [monster.monster_id for monster in tamer.tamer_party]
                Tamer_SQL_Commands.update_tamer_party(discord_id=tamer.tamer_id, tamer_party=monster_ids)
            else:
                monster_ids = [monster.monster_id for monster in tamer.tamer_monster_storage]
                Tamer_SQL_Commands.update_tamer_monster_storage(discord_id=tamer.tamer_id,
                                                                tamer_monster_storage=monster_ids)
            msg += " " + tamer_response.get('message', "")

    # Handles moving a monster from the tamer party to the monster storage
    if tamer_party is not [] and tamer_monster_storage is []:
        for monster_id in tamer_party:
            monster = InfoLoader.load_monster(monster_id=monster_id)
            if monster.monster_species_id is "":
                return general_utils.response_formatter(body={"error": f"Unable to find monster {monster_id}"},
                                                        status=404)
            tamer_response = tamer.move_monster_to_party_from_tamer_monster_storage()
            if 'error' in tamer_response:
                return general_utils.response_formatter(body=tamer_response,
                                                        status=tamer_response.get('error_code', 500))

            msg += " " + tamer_response.get('message', "")
        monster_ids = [monster.monster_id for monster in tamer.tamer_party]
        Tamer_SQL_Commands.update_tamer_party(discord_id=tamer.tamer_id, tamer_party=monster_ids)

        Tamer_SQL_Commands.update_tamer_monster_storage(discord_id=tamer.tamer_id,
                                                        tamer_monster_storage=tamer.tamer_monster_storage)

    # Handles moving a monster from the tamer monster storage to the party
    if tamer_party is [] and tamer_monster_storage is not []:
        monster_list = InfoLoader.load_monsters(tamer_monster_storage)
        for monster in monster_list:
            tamer_response = tamer.move_monster_to_party_from_tamer_monster_storage(monster)
            if 'error' in tamer_response:
                return general_utils.response_formatter(body=tamer_response,
                                                        status=tamer_response.get('error_code', 500))
            msg += " " + tamer_response.get('message', "")
        monster_ids = [monster.monster_id for monster in tamer.tamer_party]
        Tamer_SQL_Commands.update_tamer_party(discord_id=tamer.tamer_id, tamer_party=monster_ids)

        Tamer_SQL_Commands.update_tamer_monster_storage(discord_id=tamer.tamer_id,
                                                        tamer_monster_storage=tamer.tamer_monster_storage)

    return general_utils.response_formatter(body=tamer.to_dict(), status=200)
