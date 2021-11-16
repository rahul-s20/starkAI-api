from app.common.helpers.helper import keyGenerate
from app.models.keyModel import Keys
from sqlalchemy.orm import Session
from app.config.base import STARKBase
from app.schema.KeySchema import Keyssc


def assignKey(email: Keyssc, db: Session):
    try:
        stark_base = STARKBase(Keys)
        api_key = keyGenerate(keyLen=16)
        user = stark_base.get_user_by_email(db=db, email=email.email)
        if user is None:
            email.api_key = api_key
            stark_base.create(db=db, obj_in = email)
            getuser = stark_base.get_user_by_email(db=db, email=email.email)
            response = {"res": "Your api key is generated", "user": getuser}
        else:
            response = {"res": "Email is already in use, please enter a different email", "user": {}}
        return {"status": True, "type": "apiKeyGeneration", "data": response}
    except Exception as er:
        return {"status": False, "type": "apiKeyGeneration", "data": f"{er}"}
