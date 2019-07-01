import io
import os
from pdf2image import convert_from_bytes
from upload_file import upload_blob


def convert_image_object_to_bytes_io(ppmimg_obj):
    bytes_io = io.BytesIO()
    ppmimg_obj.save(bytes_io, format='jpeg')
    bytes_io.seek(0)
    return bytes_io


def convert_pdf_file_from_path_to_image(_file, path):
    all_files_paths = []
    all_files_blobs = []
    _file.seek(0)
    content = _file.read()
    pages = convert_from_bytes(content, 200)
    file_path = os.path.dirname(path)
    for indx, page in enumerate(pages):
        new_file_path = os.path.join(file_path, '{}.jpeg'.format(str(indx)))
        byte_obj = convert_image_object_to_bytes_io(page)
        # upload_blob(new_file_path, byte_obj)
        all_files_paths.append(new_file_path)
        all_files_blobs.append(byte_obj)
    return all_files_blobs, all_files_paths
