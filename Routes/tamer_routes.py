import json
import logging
import os
import sys
from datetime import datetime

from flask import Blueprint
from flask import request, Response

sys.path.append('..Models')
from Models.Tamer_Models import Tamer

sys.path.append('..utils')
from utils import general_utils
from utils.Logger import MyLogger as logger

sys.path.append('..SQL_Commands')
from SQL_Commands import Tamer_SQL_Commands

tamer_bp = Blueprint('tamer', __name__)
logger = logger()


@tamer_bp.route('/tamer', methods=['POST'])
def post_tamer():
    api_request = request.json
    discord_id=api_request.get('discord_id', None)
    if discord_id is None:
        return general_utils.response_formatter({"error": "No discord_id provided"}, 400)
    new_tamer = Tamer(discord_id=discord_id)
    Tamer_SQL_Commands.insert_tamer(discord_id=discord_id)
    if Tamer_SQL_Commands.does_tamer_exist(discord_id=discord_id):
        return general_utils.response_formatter(body={"Message":"Tamer has been created."}, status=201)
    else:
        return general_utils.response_formatter(body={"error":"Unable to insert"}, status=500)

@tamer_bp.route('/tamer/<tamer_id>', methods=['GET'])
def get_tamer(tamer_id):
    if not Tamer_SQL_Commands.does_tamer_exist(discord_id=tamer_id):
        return general_utils.response_formatter({"error": "Tamer not found"}, 404)
    tamer_json = Tamer_SQL_Commands.get_tamer(discord_id=tamer_id)[0]
    tamer = Tamer().from_json(tamer_json)

    return general_utils.response_formatter(body=json.dumps(tamer_json), status=200)






