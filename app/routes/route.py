from flask import Blueprint
from app.common.flask_ease.request_validation import validate_request
from flask import jsonify

from app.controllers.symptomController import symptomController
from app.controllers.langTranslationController import langTranslationController
from app.controllers.transcriptController import transcriptController
from app.controllers.apiKeyController import assignKey
from app.models.modalone import database
from app.controllers.csv2mysqlController import CSV2Mysql

blueprint_api = Blueprint("blueprint_api", __name__)


@blueprint_api.route("/api/v1/symptom_disease", methods=['POST'])
def symptom_route():
    symptoms = validate_request('symptoms')
    res = symptomController(symptoms)
    return res


@blueprint_api.route("/api/v1/translate", methods=['POST'])
def translation_route():
    input_text = validate_request("input_text", "destination")
    res = langTranslationController(input_text)
    return res


@blueprint_api.route("/api/v1/transcript", methods=['POST'])
def transcript_route():
    vid_id = validate_request('vid')
    res = transcriptController(vid_id)
    return res


@blueprint_api.route('/api/v1/generate_api_key', methods=['GET'])
def createAlldb():
    database.create_all()
    return jsonify(response="All tables created!")


@blueprint_api.route('/api/v1/generate_api_key', methods=['POST'])
def apiKeyGenerate_route():
    email = validate_request('email')
    res = assignKey(email=email)
    return res


@blueprint_api.route('/api/v1/migrate/csv_to_mysql', methods=['POST'])
def csv2mysql_route():
    reqdetails = validate_request('aws_details', 'mysql_details', 'content_details')
    if reqdetails['aws_details']['endpoint'] is not "":
        csvtomysql_obj = CSV2Mysql(endpoint=reqdetails['aws_details']['endpoint'],
                                   accesskey=reqdetails['aws_details']['accesskey'],
                                   secretkey=reqdetails['aws_details']['secretkey'],
                                   region=reqdetails['aws_details']['region'],
                                   usr=reqdetails['mysql_details']['user'],
                                   pwd=reqdetails['mysql_details']['password'],
                                   hst=reqdetails['mysql_details']['host'],
                                   db=reqdetails['mysql_details']['db'],
                                   )
    else:
        csvtomysql_obj = CSV2Mysql(accesskey=reqdetails['aws_details']['accesskey'],
                                   secretkey=reqdetails['aws_details']['secretkey'],
                                   usr=reqdetails['mysql_details']['user'],
                                   pwd=reqdetails['mysql_details']['password'],
                                   hst=reqdetails['mysql_details']['host'],
                                   db=reqdetails['mysql_details']['db'],
                                   )

    res = csvtomysql_obj.migrate_csv_to_mysql(bucket=reqdetails['content_details']['bucket'],
                                              key=reqdetails['content_details']['key'],
                                              columns=reqdetails['content_details']['columns'],
                                              default_values=reqdetails['content_details']['default_values'],
                                              add_primaryKey=bool(reqdetails['content_details']['add_primaryKey']),
                                              type_of_insertion=reqdetails['content_details']['type_of_insertion'],
                                              db_table=reqdetails['content_details']['db_table'],
                                              )

    return res
