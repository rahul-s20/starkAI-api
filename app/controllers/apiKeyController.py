from app.common.helpers.helper import keyGenerate
from flask import jsonify
from app.models.modalone import Keys
from app.models.modalone import database


def assignKey(email: str):
    response = {}
    try:
        api_key = keyGenerate(keyLen=16)
        user = Keys.query.filter_by(email=email["email"]).first()
        if user is None:
            newUser = Keys(api_key=api_key, email=email["email"])
            database.session.add(newUser)
            database.session.commit()
            getuser = Keys.query.filter_by(email=email["email"]).first()
            response = {"res": "Your api key is generated", "user": f"{getuser}"}
        else:
            response = {"res": "Email is already in use, please enter a different email", "user": {}}
        return {"status": True, "type": "apiKeyGeneration", "data": response}
    except Exception as er:
        return jsonify(status=False, type="apiKeyGeneration", data=f"{er}")
