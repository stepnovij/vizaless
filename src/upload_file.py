import logging
import time
from google.cloud import storage
from google.cloud.storage import Blob


def upload_blob(file_path, input_file):
    ct = time.time()
    logging.info('Start uploading file')
    """Uploads a file to the bucket."""
    client = storage.Client(project="objects-recogntion")
    bucket = client.get_bucket("recognition_documents")
    blob = Blob(file_path, bucket)
    blob.upload_from_file(input_file)
    duration = time.time() - ct
    logging.info('Finished uploading file %s', duration)


def get_blob(file_path):
    """Uploads a file to the bucket."""

    ct = time.time()
    logging.info('Start downloading file')

    client = storage.Client(project="objects-recogntion")
    bucket = client.get_bucket("recognition_documents")
    # Then do other things...
    blob = bucket.get_blob(file_path)

    duration = time.time() - ct
    logging.info('Finished downloading file %s', round(duration, 2))
    return blob.download_as_string()
