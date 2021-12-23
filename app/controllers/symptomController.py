from app.common.datapreprocessing.input_processer import input_data_scaling, input_data_conversion_symptom
from app.common.makedecision.makedecision import Decision
from app.helpers.initiater import io_symptoms
from fastapi.responses import JSONResponse
from app.schema.SymptopmSchema import SymptopmSchema


def symptomController(symptoms: SymptopmSchema) -> JSONResponse:
    '''

    :param symptoms:
    :return: predicted deases
    This the entrypoint after route to decide the deases based on the symptoms
    '''
    try:
        decision_obj = Decision(n_estimators=100, criterion='entropy')
        symptoms = symptoms.symptoms.split(",")
        ids = input_data_scaling(symptoms)
        converted_data = input_data_conversion_symptom(ids)
        response = decision_obj.deciderV2(strategy='constant', input_data=converted_data)
        res = {"status": True, "type": "symptomatic", "data": response}
        return JSONResponse(content=res)
    except Exception as er:
        res = {"status": False, "type": "symptomatic", "data": f"{er.__cause__}"}
        return JSONResponse(content=res)


def saveSymptomModelController() -> JSONResponse:
    '''

    :return: Save the symptom model based on availbe data in s3
    '''
    try:
        i_data, o_data = io_symptoms()
        decision_obj = Decision(n_estimators=100, criterion='entropy')
        res = decision_obj.saveSymptomModel(i_data=i_data, o_data=o_data, strategy='constant')
        return JSONResponse(content={"status": True, "type": "symptomatic", "data": res})
    except Exception as er:
        return JSONResponse(content={"status": False, "type": "symptomatic", "data": f"{er.__cause__}"})
