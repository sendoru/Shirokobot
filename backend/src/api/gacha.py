import pymongo
import json
import random
from flask import (
    request, make_response, Blueprint, flash
)
from ..util.gacha_util import roll_gacha

print(__name__)

gacha_prob = [0, 0.785, 0.185, 0.03]

bp = Blueprint('api/gacha', __name__, url_prefix='/api/gacha')

@bp.route('/', methods=['GET'])
async def gacha():
    if request.method == 'GET':
        gacha_type = int(request.args.get('gacha_type'))
        error = None
        if not gacha_type in (1, 10):
            return make_response("Wrong parameter gacha_type (should be 1 or 10)", 401)

        ret = roll_gacha(gacha_type)
        return make_response(ret, 200)