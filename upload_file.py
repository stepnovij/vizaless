from google.cloud import storage
from google.cloud.storage import Blob


def upload_blob(file_path, input_file):
    """Uploads a file to the bucket."""
    client = storage.Client(project="objects-recogntion")
    bucket = client.get_bucket("recognition_documents")
    blob = Blob(file_path, bucket)
    blob.upload_from_file(input_file)


def get_blob(file_path):
    """Uploads a file to the bucket."""
    client = storage.Client(project="objects-recogntion")
    bucket = client.get_bucket("recognition_documents")
    # Then do other things...
    blob = bucket.get_blob(file_path)
    return blob.download_as_string()
