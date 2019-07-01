import re
import asyncio
from upload_file import upload_blob
import time
import logging
import os
from google_vision_integration import detect_text, parse_response
from convert_to_image import convert_pdf_file_from_path_to_image
from test_abby_ocr import recognize_file
from parse_xml_response import parse_xml_response_by_path
from utils import force_async


def process_image(_file, file_path):
    tasks = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks.append(_process_image(_file, file_path))
    responses = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    parsed_response, source = responses[0]
    parsed_response.update(final_checks(parsed_response, source))
    return parsed_response


async def _process_image(_file, file_path):
    logging.info('Start process_image')

    futures = list()
    futures.append(upload_blob(file_path, _file))

    file_objs, image_paths = get_images(_file, file_path)

    passport_indx = 0

    futures.append(detect_passport_image(file_objs, image_paths))
    futures.append(recognize_file(file_objs[passport_indx], image_paths[passport_indx]))

    responses = await asyncio.gather(*futures)

    parsed_response, source = responses[1]
    file_obj = responses[2]
    parsed_response.update(parse_xml_response_by_path(file_obj))
    logging.info('Finish process_image')
    return parsed_response, source


def final_checks(parsed_response, source):
    if not parsed_response.get('IssueDate'):
        if parsed_response.get('ExpiryDate'):
            pattern = parsed_response['ExpiryDate'][:6] + '\d{4}'
            for elem in source:
                m = re.search(pattern, elem)
                if m and m.group():
                    return {'IssueDate': m.group()}
    return {}


def get_images(_file, file_path):
    logging.info('Start get_images')
    filename, file_extension = os.path.splitext(file_path)
    if file_extension == '.pdf':
        file_objs, image_paths = convert_pdf_file_from_path_to_image(_file, file_path)
    else:
        _file.seek(0)
        file_objs, image_paths = [_file], [file_path]
    logging.info('Finish get_images')
    return file_objs, image_paths


@force_async
def detect_passport_image(file_objs, image_paths):
    ct = time.time()
    source = []
    logging.info('start detect_passport_image')
    all_text = []
    parsed_response = dict()
    for idx, image_path in enumerate(image_paths):
        detected_text = detect_text(file_objs[idx])
        all_text.append(detected_text)

    passport_indx = 0
    for idx, text in enumerate(all_text):
        parsed_response, source = parse_response(text)
        # if 'passport' in text.lower() and 'name' in text.lower() and '<<<<' in text:
            # parsed_response = parse_response(text)
            # passport_indx = idx
            # break

    duration = time.time() - ct
    logging.info('finished detect_passport_image duration %s', str(round(duration, 2)))
    return parsed_response, source#, passport_indx