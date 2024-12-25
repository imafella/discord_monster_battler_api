import logging
import os
import sys
from datetime import datetime

from flask import Blueprint
from flask import request, Response

sys.path.append('..Models')
from Models.Battle_Models import Battle

sys.path.append('..utils')
from utils import general_utils

logging.basicConfig(
    filename=f"{datetime.now().strftime('%Y-%m-%d')}_tamer.log",
    format='%(asctime)s %(message)s',
    filemode='w'
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
response_format = os.environ.get('battle_routes_response_format', 'application/json')

battle_bp = Blueprint('tamer', __name__)


@battle_bp.route('/tamer', methods=['POST'])
def post_battle():
    api_request = request.json
    initiating_tamer_id = api_request.get("initiating_id", None)
    new_battle = Battle(initiating_id=initiating_tamer_id, target_id=api_request.get('target_id', None))
    if initiating_tamer_id is None:
        logger.debug(f"{new_battle.battle_id} was not provided initiating_id. Marking as closed")
        new_battle.is_active = False
        return general_utils.response_formatter(general_utils.obj_to_dict(new_battle), status=400)




