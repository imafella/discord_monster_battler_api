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

tamer_bp = Blueprint('tamer', __name__)
logger = logger()


@tamer_bp.route('/tamer', methods=['POST'])
def post_tamer():
    api_request = request.json
    discord_id=api_request.get('discord_id', None)
    if discord_id is None:
        return general_utils.response_formatter({"error": "No discord_id provided"}, 400)
    new_tamer = Tamer(discord_id=discord_id)





