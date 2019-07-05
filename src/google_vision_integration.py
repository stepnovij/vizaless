import re
from google.cloud import vision
from transliterate import translit

from utils import is_date_valid


def detect_text(file_obj):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    file_obj.seek(0)
    content = file_obj.read()
    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description


def _preprocess_data(data):
    data = data.replace('|', "/")
    data = data.upper()
    data = data.replace('ГОР.', '')
    # englisch characters:
    data = data.replace('M / M', '')
    data = data.replace('M /M', '')
    data = data.replace('M/M', '')
    data = data.replace('M/ M', '')
    #
    # russian characters:
    data = data.replace('М / М', '')
    data = data.replace('М /М', '')
    data = data.replace('М/М', '')
    data = data.replace('М/ М', '')
    #
    data = data.replace('Ж / F', '')
    data = data.replace('Ж /F', '')
    data = data.replace('Ж/F', '')
    data = data.replace('Ж/ F', '')
    #
    data = data.replace('X / F', '')
    data = data.replace('X /F', '')
    data = data.replace('X/F', '')
    data = data.replace('X/ F', '')

    data = re.sub(r'\s\w{1}/\w{1}\s', '\n', data, flags=re.DOTALL)

    data = re.sub(r'\sF\s', ' ', data, flags=re.DOTALL)
    data = re.sub(r'\sЖ\s', ' ', data, flags=re.DOTALL)
    data = re.sub(r'\sМ\s', ' ', data, flags=re.DOTALL)
    data = re.sub(r'\sM\s', ' ', data, flags=re.DOTALL)

    data = data.replace('!', '')
    data = data.replace('?', '')

    data = data.replace('Г.', '')
    data = data.replace('ГОР.', '')
    return data


def has_issue_organization(elem):
    if 'ФМС' in elem or 'МВД' in elem:
        return True
    return False


def get_issue_organization(elem, data_array, idx):
    issue_dict = dict()

    # Logic1
    if 'ISSUE' in elem:
        if is_date_valid(data_array[idx + 2]):
            issue_dict['IssueDate'] = data_array[idx + 2]
        if has_issue_organization(data_array[idx + 3]):
            issue_dict['IssuerOrganization'] = data_array[idx + 3].replace(' ', '')
            issue_dict['IssuerOrganizationTranslit'] = translit(issue_dict['IssuerOrganization'], 'ru', reversed=True)

    # Logic2
    if has_issue_organization(elem):
        issue_dict['IssuerOrganization'] = elem.replace(' ', '')
        issue_dict['IssuerOrganizationTranslit'] = translit(issue_dict['IssuerOrganization'], 'ru', reversed=True)
    return issue_dict


def has_all_issue_keys(final_dict):
    if 'IssueDate' in final_dict  and 'IssuerOrganization' in final_dict:
        return True
    return False


def has_all_birth_keys(final_dict):
    if 'PlaceOfBirthCity' in final_dict and 'PlaceOfBirthCountry' in final_dict:
        return True
    return False


def get_place_of_birth(elem, data_array, idx):
    birth_dict = dict()

    if 'МОСКВА' in elem:
        birth_dict['PlaceOfBirthCity'] = 'МОСКВА'

    # Logic1
    if 'USSR' in elem:
        birth_dict['PlaceOfBirthCountry'] = 'USSR'
        birth_dict['PlaceOfBirthCity'] = elem.split('/', maxsplit=1)[0].strip()

    if 'RUSSIA' in elem and 'RUSSIAN' not in elem:
        birth_dict['PlaceOfBirthCountry'] = 'RUSSIA'

    if 'GEORGIA' in elem:
        birth_dict['PlaceOfBirthCountry'] = 'GEORGIA'

    if has_all_birth_keys(birth_dict):
        birth_dict['PlaceOfBirthCityTranslit'] = translit(birth_dict['PlaceOfBirthCity'], 'ru', reversed=True).strip().upper()
        return birth_dict

    # Logic1
    if ('RUSSIA' in elem and 'RUSSIAN' not in elem) or 'USSR' in elem:
        possible_city = elem.split('/')[0]
        birth_dict['PlaceOfBirthCity'] = possible_city.strip()

    if has_all_birth_keys(birth_dict):
        birth_dict['PlaceOfBirthCityTranslit'] = translit(birth_dict['PlaceOfBirthCity'], 'ru', reversed=True).strip().upper()
        return birth_dict

    # Logic3
    if 'PLACE OF BIRTH' in elem:
        place_of_birth_str = data_array[idx + 1]
        obj = place_of_birth_str.strip().split('/')
        if len(obj) == 2:
            city, country = obj
        else:
            city = ''
            country = ' '.join(obj)
        birth_dict['PlaceOfBirthCity'] = city.strip().replace('Г.', '')
        birth_dict['PlaceOfBirthCountry'] = country.strip()

    if 'PlaceOfBirthCity' in birth_dict:
        birth_dict['PlaceOfBirthCityTranslit'] = translit(birth_dict['PlaceOfBirthCity'], 'ru', reversed=True).strip().upper()
        birth_dict['PlaceOfBirthCity'] = birth_dict['PlaceOfBirthCity'].strip()
    return birth_dict


def remove_non_cyrillic(text):
    return ''.join([l.group() for l in [re.search('[а-яА-Я\s]', x) for x in text] if l]).strip()


def remove_all_non_cyrillic_symb(final_dict):
    if 'LastNameRus' in final_dict:
        final_dict['LastNameRus'] = remove_non_cyrillic(final_dict['LastNameRus'])
    if 'FirstNameFatherNameRus' in final_dict:
        final_dict['FirstNameFatherNameRus'] = remove_non_cyrillic(final_dict['FirstNameFatherNameRus'])
    return final_dict


def parse_response(data):
    final_dict = {}

    data = _preprocess_data(data)
    data_array = data.strip().split('\n')
    for idx, elem in enumerate(data_array):

        if ('SURNAME' in elem or 'ФАМИЛИЯ' in elem):
            family_name = data_array[idx + 1].split(' ')[0]
            final_dict['LastNameRus'] = ''.join([val for val in family_name if val.isalpha()])

        if 'GIVEN' in elem or 'NAMES' in elem:
            final_dict['FirstNameFatherNameRus'] = data_array[idx + 1].replace('/', '').strip()

        #awesome logic with multiple rewritings
        birth_dict = get_place_of_birth(elem, data_array, idx)
        final_dict.update(birth_dict)

        if not has_all_issue_keys(final_dict):
            issue_dict = get_issue_organization(elem, data_array, idx)
            final_dict.update(issue_dict)

    if not final_dict.get('PlaceOfBirthCityTranslit'):
        final_dict['PlaceOfBirthCityTranslit'] = ''
    final_dict = remove_all_non_cyrillic_symb(final_dict)
    return final_dict, data_array

