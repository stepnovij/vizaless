import io
from google.cloud import vision
from transliterate import translit
from upload_file import get_blob


data = """
РОССИЙСКАЯ ФЕДЕРАЦИЯ
RUSSIAN FEDERATION
RUS
АН-Подпись владельца
Holder's signature
RUS
suing State
РоссийсКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION
ПАСПОРТ PASSPORT Ти/Type Код государства/Code of Номер паспорта Passport No
даа
71 8559738
Фамилия / Surname
МИШЕЧКИНА 1
MISHECHKINA
West Given names
АННА БОРИСОВНА /
ANNA
Гражданство / Nationality
РоссийскАЯ ФЕДЕРАЦИЯ / RussIAN FEDERATION
Дата рождения / Date of birth
Учетная запись
06.08.1991
Пол/ Sex Место рождения / Place of birth
Ж/Е ГОР. САМАРА / USSR
Дата выдачи / Dute of issue
Орган, выдавший документ /Authority
07.04.2012
ФМС 63007
Дата окончания срока Datar of expiry
Подтись владельца / Holder's signature
действия
07.04.2022
P<RUSMISHECHKINA<<ANNA<<<<<<<<<<<<<<<<<<<<<<
7185597385RUS9108068F2204075<<<<<<<<<<<<<<04
"""


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    content = get_blob(path)

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description


def parse_response(data):
    final_dict = {}
    data_array = data.strip().split('\n')

    for idx, elem in enumerate(data_array):
        if 'place of birth' in elem.lower():
            place_of_birth_str = data_array[idx+1]
            obj = place_of_birth_str[3:].strip().split('/')
            if len(obj) == 2:
                city, country = obj
            else:
                city = ''
                country = ' '.join(obj)
            final_dict['PlaceOfBirthCity'] = city.strip()
            final_dict['PlaceOfBirthCityTranslit'] = translit(city.strip(), 'ru', reversed=True)
            final_dict['PlaceOfBirthCountry'] = country.strip()

        if 'date of issue' in elem.lower():
            final_dict['IssueDate'] = data_array[idx+2]
            final_dict['IssuerOrganization'] = data_array[idx+3].replace(' ','')
            final_dict['IssuerOrganizationTranslit'] = translit(data_array[idx+3].replace(' ',''), 'ru', reversed=True)
    return final_dict

