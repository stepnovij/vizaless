import os

amo_apikey = 'c89f969da9eb1c2db634d8f1a28cde2ef431afba'
amo_user = 'stepnovij'
amo_email = 'stepnovij@gmail.com'
APPLICATION_ID = 'stepnovij_recognition_test'
APPLICATION_PASSWORD = 'GUEwDXhpgz3COGUrFbMyRHTc'


UPLOAD_GOOGLE_PROJECT = 'objects-recogntion'
UPLOAD_GOOGLE_BUCKET_NAME = 'recognition_documents'
UPLOAD_TEST_PATH = 'test'


def is_dev_env():
    cur_env = os.getenv('FLASK_ENV')
    if cur_env == 'development':
        return True
    return False
