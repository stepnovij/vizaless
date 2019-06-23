from google_vision_integration import detect_text, parse_response
from convert_to_image import convert_pdf_file_from_path_to_image
from test_abby_ocr import recognize_file
from parse_xml_response import parse_xml_response_by_path


def get_recognized_id(path):
    all_text = []
    parsed_response = dict()

    image_paths = convert_pdf_file_from_path_to_image(path)

    for image_path in image_paths:
        detected_text = detect_text(image_path)
        all_text.append(detected_text)

    passport_indx = None
    for idx, text in enumerate(all_text):
        if 'passport' in text.lower() and 'name' in text.lower() and '<<<<' in text:
            parsed_response = parse_response(text)
            passport_indx = idx
            break
    print(image_paths)
    target_file = recognize_file(image_paths[0])
    parsed_response.update(parse_xml_response_by_path(target_file))
    return parsed_response