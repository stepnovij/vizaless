import io
import time
import logging
import os
from google_vision_integration import detect_text, parse_response
from convert_to_image import convert_pdf_file_from_path_to_image
from test_abby_ocr import recognize_file
from parse_xml_response import parse_xml_response_by_path


def process_image(_file, file_path):
    logging.info('Start process_image')
    # bytes_io = io.StringIO()
    # _file.save(bytes_io)
    # bytes_io.seek(0)

    file_objs, image_paths = get_images(_file, file_path)

    # TODO: make here real detect algorithm of the passport:
    parsed_response, passport_indx = detect_passport_image(file_objs, image_paths)
    target_file = recognize_file(file_objs[passport_indx], image_paths[passport_indx])

    parsed_response.update(parse_xml_response_by_path(target_file))
    logging.info('Finish process_image')
    return parsed_response


def get_images(_file, file_path):
    logging.info('Start get_image_paths')
    filename, file_extension = os.path.splitext(file_path)
    if file_extension == '.pdf':
        file_objs, image_paths = convert_pdf_file_from_path_to_image(_file, file_path)
    else:
        _file.seek(0)
        file_objs, image_paths = [_file], [file_path]
    logging.info('Finish get_image_paths')
    return file_objs, image_paths


def detect_passport_image(file_objs, image_paths):
    ct = time.time()
    logging.info('start detect_passport_image')
    all_text = []
    parsed_response = dict()
    for idx, image_path in enumerate(image_paths):
        detected_text = detect_text(file_objs[idx])
        all_text.append(detected_text)

    passport_indx = 0
    for idx, text in enumerate(all_text):
        if 'passport' in text.lower() and 'name' in text.lower() and '<<<<' in text:
            parsed_response = parse_response(text)
            passport_indx = idx
            break
    duration = time.time() - ct
    logging.info('finished detect_passport_image duration %s', str(round(duration, 2)))
    return parsed_response, passport_indx