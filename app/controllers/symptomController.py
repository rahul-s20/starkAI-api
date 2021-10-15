from flask import jsonify
from app.common.datapreprocessing.input_processer import input_data_scaling, input_data_conversion_symptom
from app.common.makedecision.makedecision import Decision
from app.helpers.initiater import symptometic_response_init


def symptomController(symptoms):
    try:
        i_data, o_data = symptometic_response_init()
        decision_obj = Decision(n_estimators=100, criterion='entropy')
        symptoms = symptoms['symptoms'].split(",")
        ids = input_data_scaling(symptoms)
        converted_data = input_data_conversion_symptom(ids)
        response = decision_obj.decider(i_data=i_data, o_data=o_data, strategy='constant', input_data=converted_data)
        return jsonify(status= True, type= "symptomatic", data= response)
    except Exception as er:
        return jsonify(status=True, type="symptomatic", data=f"{er}")
