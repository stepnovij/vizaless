from amo_crm_integration import add_contact_to_lead
from datetime import datetime
from recognizer import get_recognized_id
from flask import Flask, request, json, render_template, abort
from upload_file import upload_blob


app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route('/upload', methods=['POST'])
def recognize_data():
    f = request.files['the_file']
    _file_path = '{}/'.format(datetime.now().timestamp())
    file_path = _file_path + f.filename
    upload_blob(file_path, f)
    file_dict = get_recognized_id(file_path)
    return json.dumps(file_dict)


@app.route('/upload_crm', methods=['POST'])
def upload_to_crm():
    """
    curl -H "Content-Type: application/json"  -X POST 'http://127.0.0.1:5000/upload_crm' -d '{"BirthDate": "06.08.1991", "ExpiryDate": "07.04.2022", "GivenName": "ANNA", "IssueDate": "07.04.2012", "IssuerOrganization": "\\u0424\\u041c\\u042163007", "IssuerOrganizationTranslit": "FMS63007", "LastName": "MISHECHKINA", "Nationality": "RUS", "PlaceOfBirthCity": "\\u0413\\u041e\\u0420. \\u0421\\u0410\\u041c\\u0410\\u0420\\u0410", "PlaceOfBirthCityTranslit": "GOR. SAMARA", "PlaceOfBirthCountry": "USSR", "lead_id": "3787601", "DocumentNumber": "718559738"}'
    """
    request_data = json.loads(request.data)
    lead_id = request_data.get('lead_id')
    if not lead_id:
        abort(400)
    resp = add_contact_to_lead(lead_id, request_data)
    return json.dumps({"id": resp})


@app.route('/')
def root():
    return render_template('/index.html', title="Home")
