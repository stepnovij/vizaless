import os
import logging
import time
from google.cloud import storage
from google.cloud.storage import Blob
from utils import force_async

from settings import UPLOAD_GOOGLE_PROJECT, UPLOAD_GOOGLE_BUCKET_NAME, UPLOAD_TEST_PATH, is_dev_env


@force_async
def upload_blob(file_path, input_file):
    ct = time.time()
    logging.info('Start uploading file')
    """Uploads a file to the bucket."""
    client = storage.Client(project=UPLOAD_GOOGLE_PROJECT)
    bucket = client.get_bucket(UPLOAD_GOOGLE_BUCKET_NAME)
    if is_dev_env:
        file_path = os.path.join(UPLOAD_TEST_PATH, file_path)
    blob = Blob(file_path, bucket)
    input_file.seek(0)
    blob.upload_from_file(input_file)
    duration = time.time() - ct
    logging.info('Finished uploading file %s', duration)


def get_blob(file_path):
    """Uploads a file to the bucket."""

    ct = time.time()
    logging.info('Start downloading file')

    client = storage.Client(project=UPLOAD_GOOGLE_PROJECT)
    bucket = client.get_bucket(UPLOAD_GOOGLE_BUCKET_NAME)
    # Then do other things...
    if is_dev_env:
        file_path = os.path.join(UPLOAD_TEST_PATH, file_path)
    blob = bucket.get_blob(file_path)

    duration = time.time() - ct
    logging.info('Finished downloading file %s', round(duration, 2))
    return blob.download_as_string()
