import os
import logging
import time
from amo_crm_integration import add_contact_to_lead
from datetime import datetime
from recognizer import process_image
from flask import Flask, request, json, render_template
from upload_file import upload_blob
from werkzeug.exceptions import BadRequest
from exceptions import InvalidUsage
from flask import jsonify
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__, static_folder="static", template_folder="templates")


EXTENSIONS = ('.pdf', '.jpeg', '.jpg', '.png')


@app.route('/upload', methods=['POST'])
def recognize_data():
    ct = time.time()
    f = request.files.get('the_file')
    if not f:
        raise InvalidUsage('Please attach file and send it!', status_code=400)
    file_path = get_file_path(f)
    validate_image(file_path)
    upload_blob(file_path, f)
    file_dict = process_image(file_path)
    duration = round(time.time() - ct, 2)
    logging.info('Total duration time %s', duration)
    return json.dumps(file_dict)


def get_file_path(f):
    _file_path = '{}/'.format(datetime.now().timestamp())
    file_path = _file_path + f.filename
    return file_path


def validate_image(file_path):
    filename, file_extension = os.path.splitext(file_path)
    if file_extension not in EXTENSIONS:
        raise InvalidUsage('Not proper file format. Please use: PDF, JPEG, JPG, PNG', status_code=400)


@app.route('/upload_crm', methods=['POST'])
def upload_to_crm():
    """
    curl -H "Content-Type: application/json"  -X POST 'http://127.0.0.1:5000/upload_crm' -d '{"BirthDate": "06.08.1991", "ExpiryDate": "07.04.2022", "GivenName": "ANNA", "IssueDate": "07.04.2012", "IssuerOrganization": "\\u0424\\u041c\\u042163007", "IssuerOrganizationTranslit": "FMS63007", "LastName": "MISHECHKINA", "Nationality": "RUS", "PlaceOfBirthCity": "\\u0413\\u041e\\u0420. \\u0421\\u0410\\u041c\\u0410\\u0420\\u0410", "PlaceOfBirthCityTranslit": "GOR. SAMARA", "PlaceOfBirthCountry": "USSR", "lead_id": "3787601", "DocumentNumber": "718559738"}'
    """
    request_data = json.loads(request.data)
    lead_id = request_data.get('lead_id')
    if not lead_id:
        raise BadRequest('No lead_id is provided')
    resp = add_contact_to_lead(lead_id, request_data)
    return json.dumps({"id": resp})


@app.route('/')
def root():
    logging.info('root handler')
    return render_template('/index.html', title="Home")


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
