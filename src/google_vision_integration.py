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
        birth_dict['PlaceOfBirthCityTranslit'] = translit(birth_dict['PlaceOfBirthCity'], 'ru', reversed=True)

    # Logic1
    if 'USSR' in elem:
        birth_dict['PlaceOfBirthCountry'] = 'USSR'
        possible_city = elem.split('/')[:1]

    if 'RUSSIA' in elem and 'RUSSIAN' not in elem:
        birth_dict['PlaceOfBirthCountry'] = 'RUSSIA'

    if 'GEORGIA' in elem:
        birth_dict['PlaceOfBirthCountry'] = 'GEORGIA'

    if has_all_birth_keys(birth_dict):
        return birth_dict

    # Logic1
    if 'RUSSIA' in elem and 'RUSSIAN' not in elem:
        possible_city, _ = elem.split('/')[:1]
        if 'Г.' in possible_city:
            city = elem.split('Г.')[-1].strip().replace('Г.')
            birth_dict['PlaceOfBirthCity'] = city.strip()
            birth_dict['PlaceOfBirthCityTranslit'] = translit(birth_dict['PlaceOfBirthCity'], 'ru', reversed=True).upper()

    if has_all_birth_keys(birth_dict):
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
        birth_dict['PlaceOfBirthCityTranslit'] = translit(birth_dict['PlaceOfBirthCity'], 'ru', reversed=True).upper()
        birth_dict['PlaceOfBirthCountry'] = country.strip()
    return birth_dict


def parse_response(data):
    final_dict = {}

    data = _preprocess_data(data)
    data_array = data.strip().split('\n')

    print('HERE:')
    print(data_array)
    for idx, elem in enumerate(data_array):

        if 'SURNAME' in elem:
            final_dict['LastNameRus'] = ''.join([val for val in data_array[idx+1] if val.isalpha()])

        if 'GIVEN' in elem:
            final_dict['FirstNameFatherNameRus'] = data_array[idx + 1].replace('/', '').strip()

        #awesome logic with multiple rewritings
        birth_dict = get_place_of_birth(elem, data_array, idx)
        final_dict.update(birth_dict)

        if not has_all_issue_keys(final_dict):
            issue_dict = get_issue_organization(elem, data_array, idx)
            final_dict.update(issue_dict)

    if not final_dict.get('PlaceOfBirthCityTranslit'):
        final_dict['PlaceOfBirthCityTranslit'] = ''
    return final_dict, data_array

