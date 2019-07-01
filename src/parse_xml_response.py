import pycountry
import xml.dom.minidom
from upload_file import get_blob


def parse_xml_response_by_path(fs):
    needed_keys = {
        'LastName',
        'GivenName',
        'Nationality',
        'BirthDate',
        'ExpiryDate',
        'DocumentNumber',
    }
    dom = xml.dom.minidom.parseString(fs)
    parsed_resp = dict()
    for elem in dom.firstChild.getElementsByTagName('field'):
        attr = elem.getAttribute('type')
        if attr in needed_keys:
            value = elem.getElementsByTagName('value')[0].firstChild.data
            if attr in ('BirthDate', 'ExpiryDate'):
                value_year = value[0:2]
                value_month = value[2:4]
                value_date = value[4:6]
                if attr == 'ExpiryDate':
                    value_year = '20' + value_year
                if attr == 'BirthDate':
                    if int(value_year) > 20:
                        value_year = '19' + value_year
                    else:
                        value_year = '20' + value_year
                value = '{}.{}.{}'.format(value_date, value_month, value_year)
            if attr == 'Nationality':
                value = pycountry.countries.get(alpha_3=value).name
            parsed_resp[attr] = value
    return parsed_resp
