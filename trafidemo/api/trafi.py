from flask import jsonify, Blueprint
from flask_login import login_required, login_user, logout_user
import pymongo

blueprint = Blueprint('api', __name__, url_prefix='/api', static_folder='../static')

client = pymongo.MongoClient()
db = client.lz_trafi
citycollectionfinal = db.carsbycityfinal

@blueprint.route('/trafi/<string:municipal>/', methods=['GET'])
@blueprint.route('/trafi/', methods=['GET'])
def trafi(municipal=None):

    if municipal:
        data = citycollectionfinal.find_one({"kunta": municipal}, {"_id": 0})
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
        cursor = citycollectionfinal.find({}, {"_id": 0}).sort([('kunta', pymongo.ASCENDING)])
        data = []
        for m in cursor:
            data.append(m)
        return jsonify({"data": data})




