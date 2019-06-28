import os
from google_vision_integration import detect_text, parse_response
from convert_to_image import convert_pdf_file_from_path_to_image
from test_abby_ocr import recognize_file
from parse_xml_response import parse_xml_response_by_path


def process_image(file_path):
    parsed_response = dict()
    image_paths = get_image_paths(file_path)
    # TODO: make here real detect algorithm of the passport:
    passport_indx = 0
    target_file = recognize_file(image_paths[passport_indx])
    parsed_response.update(parse_xml_response_by_path(target_file))
    return parsed_response


def get_image_paths(file_path):
    filename, file_extension = os.path.splitext(file_path)
    if file_extension == 'pdf':
        image_paths = convert_pdf_file_from_path_to_image(file_path)
    else:
        image_paths = [file_path]
    return image_paths


def detect_passport_image(image_paths):
    all_text = []
    for image_path in image_paths:
        detected_text = detect_text(image_path)
        all_text.append(detected_text)

    passport_indx = None
    for idx, text in enumerate(all_text):
        if 'passport' in text.lower() and 'name' in text.lower() and '<<<<' in text:
            parsed_response = parse_response(text)
            passport_indx = idx
            break
    return passport_indx