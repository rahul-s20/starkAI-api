from app.common.translator.language_translate import LanguageTranslate
from app.schema.TranslateSchema import TranslateSchema
from fastapi.responses import JSONResponse


def langTranslationController(input_text: TranslateSchema) -> JSONResponse:
    try:
        response_obj = LanguageTranslate()
        response = response_obj.tras_lation(input_text=input_text.input_text, dest=input_text.destination)
        res = {"status": True, "type": "translatotr", "data": response}
        return JSONResponse(content=res)
    except Exception as er:
        res = {"status": False, "type": "translatotr", "data": f"{er}"}
        return JSONResponse(content=res)
