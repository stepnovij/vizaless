import os

amo_apikey = 'b2507319599db3130bd5512c3d749ad8f87c2663'
amo_user = 'stanrubovskiy'
amo_email = 'stan.rubovskiy@gmail.com'


VERSION = 'moscow-viza'
# VERSION = 'emails'

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
