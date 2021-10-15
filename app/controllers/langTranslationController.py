from app.common.translator.language_translate import LanguageTranslate
from flask import jsonify


def langTranslationController(input_text:str) -> dict:
    try:
        response_obj = LanguageTranslate()
        response = response_obj.tras_lation(input_text=input_text['input_text'], dest=input_text['destination'])
        return jsonify(status= True, type= "translatotr", data= response)
    except Exception as er:
        return jsonify(status= False, type= "translatotr", data= f"{er}")
