from amocrm import BaseContact, BaseLead, amo_settings, fields

from settings import amo_apikey, amo_user, amo_email

amo_settings.set(amo_email, amo_apikey, amo_user)


class Contact(BaseContact):
    leads_model = BaseLead
    first_name = fields.CustomField(u'Имя')
    last_name = fields.CustomField(u'Фамилия')
    birth_date = fields.CustomField(u'Дата рождения')
    passport_number = fields.CustomField(u'Номер паспорта')
    issue_date = fields.CustomField(u'Дата выдачи')
    expiry_date = fields.CustomField(u'Дата окончания')
    issue_organization_translit = fields.CustomField(u'Орган выдавший документ')
    place_of_birth_country = fields.CustomField(u'Страна рождения')
    place_of_birth_city = fields.CustomField(u'Город рождения')
    nationality = fields.CustomField(u'Национальность')


def add_contact_to_lead(lead_id, contact_info):
    lead = BaseLead.objects.search(lead_id)[0]
    new_contact = Contact(
        name=contact_info.get('GivenName'),
        last_name=contact_info.get('LastName'),
        passport_number=contact_info.get('DocumentNumber'),
        birth_date=contact_info.get('BirthDate'),
        issue_date=contact_info.get('IssueDate'),
        expiry_date=contact_info.get('ExpiryDate'),
        issue_organization_translit=contact_info.get('IssuerOrganizationTranslit'),
        place_of_birth_country=contact_info.get('PlaceOfBirthCountry'),
        place_of_birth_city=contact_info.get('PlaceOfBirthCityTranslit'),
        nationality=contact_info.get('Nationality'),
    )
    new_contact.save()
    new_contact.leads = [lead]
    new_contact.save()
    return new_contact.id

