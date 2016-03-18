from flask import jsonify, Blueprint
from flask_login import login_required, login_user, logout_user
import pymongo

blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')

client = pymongo.MongoClient()
db = client.lz_trafi
autotcollection = db.autotkunnittain


@blueprint.route('/trafi/<string:municipal>/<string:year>/', methods=['GET'])
@blueprint.route('/trafi/<string:municipal>/', methods=['GET'])
@blueprint.route('/trafi/', methods=['GET'])
def trafi(municipal=None, year=None):

    if year:
        data = autotcollection.find_one({"kunta": municipal, "vuosi": year}, {"_id": 0})
        if data:
            return jsonify({
                "status": "ok",
                "data": data
            })
        else:
            return jsonify({"status": "not found",
                    "response": "kuntaa {} ei löydy".format(municipal)
                    })
    elif municipal:
        data = autotcollection.find_one({"kunta": municipal}, {"_id": 0})
        if data:
            return jsonify({
                "status": "ok",
                "data": data
            })
        else:
            return jsonify({"status": "not found",
                    "response": "kuntaa {} ei löydy".format(municipal)
                    })
    else:
        cursor = autotcollection.find({"vuosi": ''}, {"_id": 0}).sort([('kunta', pymongo.ASCENDING)])
        data = []
        for m in cursor:
            data.append(m)
        return jsonify({"data": data})




