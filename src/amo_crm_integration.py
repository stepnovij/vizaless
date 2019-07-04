from amocrm import BaseContact, BaseLead, amo_settings, fields

from settings import amo_apikey, amo_user, amo_email

amo_settings.set(amo_email, amo_apikey, amo_user)


class Contact(BaseContact):
    leads_model = BaseLead
    first_name = fields.CustomField(u'Имя')
    last_name = fields.CustomField(u'Фамилия')
    birth_date = fields.CustomField(u'День Рождения')
    passport_number = fields.CustomField(u'Номер Паспорта')
    issue_date = fields.CustomField(u'Дата Выдачи')
    expiry_date = fields.CustomField(u'Дата окончания')
    issue_organization_translit = fields.CustomField(u'Документ Выдан')
    place_of_birth = fields.CustomField(u'Место рождения')
    nationality = fields.CustomField(u'Гражданство')
    fio = fields.CustomField(u'Имя контакта')
    fio_2 = fields.CustomField(u'Фамилия И.О.')


def add_contact_to_lead(lead_id, contact_info):
    lead = BaseLead.objects.search(lead_id)[0]
    new_contact = Contact(
        name=contact_info.get("FIO_2"),
        first_name=contact_info.get("GivenName"),
        last_name=contact_info.get('LastName'),
        passport_number=contact_info.get('DocumentNumber'),
        birth_date=contact_info.get('BirthDate'),
        issue_date=contact_info.get('IssueDate'),
        expiry_date=contact_info.get('ExpiryDate'),
        issue_organization_translit=contact_info.get('IssuerOrganizationTranslit'),
        place_of_birth=contact_info.get('PlaceOfBirthTranslit'),
        nationality=contact_info.get('Nationality'),
        fio=contact_info.get("FIO"),
        fio_2=contact_info.get("FIO_2")
    )
    new_contact.save()
    new_contact.leads = [lead]
    new_contact.save()
    return new_contact.id

