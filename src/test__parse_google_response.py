import unittest
from google_vision_integration import parse_response


class TestGoogleRecognize(unittest.TestCase):

    def test__parse_google_response1(self):
        google_response = "КІРІ АРНА\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nУЛ\nI RUS\nПОДПИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\nРОССИЙСКАЯ ФЕДЕРАЦИЯ /RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT TUN/TYPE КОД ГОСУДАРСТВА/CODE OF НОМЕР ПАСПОРТА/PASSPORT NO.\n7 UING STATE 73 6153266\nР\nRUS\nФАМИЛИЯ / SURNAME\nЧЕРВИНСКАЯ І\nCHERVINSKAIA\nWE GIVEN NAMES\nЛИДИЯ ВЛАДИМИРОВНА /\nLIDITA\nГРАЖДАНСТВО /NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nДАТА РОЖДЕН /DATE OF BIRTH\nУЧЕТНАЯ ЗАПИСЬ\n21.11.1983\nПОЛ /SEX МЕСТО РОЖДЕНИЯ / PLACE OF BIRTH\nK/F КРАСНОЯРСКИЙ КРАЙ / USSR\nДАТА ВЫДАЧИ /DATE OF THE\nОРГАН, ВЫДАВШИЯ ДОКУМЕНТ/AUTHORITY\n01.10.2014\nФМС 24009\nДАТА ОКОНЧАНИЯ СРОКА ONTE OF EXPIRY\nПОДПИСЬ ИЛ ДЕЛЬВА/HOLDERS AGNATURE\nДЕЙСТВИЯ\n01.10.2024\nP<RUS CHERVINSKAIA<<LIDIIA<<<<<<<<<<<<<<<<<<<\n7361532667 RUS 831 121OF2410018<<<<<<<<<<<<<<06"
        final_dict, data_array = parse_response(google_response)
        resp = {'LastNameRus': 'ЧЕРВИНСКАЯ', 'FirstNameFatherNameRus': 'ЛИДИЯ ВЛАДИМИРОВНА', 'PlaceOfBirthCity': 'КРАСНОЯРСКИЙ КРАЙ', 'PlaceOfBirthCityTranslit': 'KRASNOJARSKIJ KRAJ', 'PlaceOfBirthCountry': 'USSR', 'IssuerOrganization': 'ФМС24009', 'IssuerOrganizationTranslit': 'FMS24009'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response2(self):
        google_response = "РОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nRUS\nАН-Подпись владельца\nHolder's signature\nRUS\nsuing State\nРоссийсКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nПАСПОРТ PASSPORT Ти/Type Код государства/Code of Номер паспорта Passport No\nдаа\n71 8559738\nФамилия / Surname\nМИШЕЧКИНА 1\nMISHECHKINA\nWest Given names\nАННА БОРИСОВНА /\nANNA\nГражданство / Nationality\nРоссийскАЯ ФЕДЕРАЦИЯ / RussIAN FEDERATION\nДата рождения / Date of birth\nУчетная запись\n06.08.1991\nПол/ Sex Место рождения / Place of birth\nЖ/Е ГОР. САМАРА / USSR\nДата выдачи / Dute of issue\nОрган, выдавший документ /Authority\n07.04.2012\nФМС 63007\nДата окончания срока Datar of expiry\nПодтись владельца / Holder's signature\nдействия\n07.04.2022\nP<RUSMISHECHKINA<<ANNA<<<<<<<<<<<<<<<<<<<<<<\n7185597385RUS9108068F2204075<<<<<<<<<<<<<<04"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'АННА БОРИСОВНА', 'IssueDate': '07.04.2012', 'IssuerOrganization': 'ФМС63007',
                'IssuerOrganizationTranslit': 'FMS63007', 'LastNameRus': 'МИШЕЧКИНА', 'PlaceOfBirthCity': 'САМАРА',
                'PlaceOfBirthCityTranslit': 'SAMARA', 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response3(self):
        google_response = "ги на\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\n(RUS\nПодпись владельца\nHolder's signature\nВыдачи\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nПАСПОРТ /PASSPORT\nTen/ Type Код Государства/Code of — Номер паспорта/Passport No.\nissuing State\nRUS\n72 3336943\nФамилия / Surname\nВЯЛЬЦЕВА /\nVYALTSEVA\nИлля / Given names\nЕЛЕНА НИКОЛАЕВНА |\nELENA\nГражданство/Nationality\nРоссийскАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nДата рождения /Date of birth\nУчетная запись\n15.03.1958\nПол/Sex-\nМесто рождения /Place of birth\nX/F МосковскАЯ ОБЛ. / USSR\nДата выдачи/Date of issue\nОрган, выдавший документ /Authority\n01.03.2013\nФМС 77207\nДата окончания срока / Date of expiry\nПодпись владельца /Holder's signature\nдействия\n01.03.2023\nбор. д.\nP< RUSVYALTSEVA<<ELENA<<<<<<<<<<<<<<<<<<<<<<<\n7233369432 RUS 5803158F2303015<<<<<<<<<<<<<<02"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'ЕЛЕНА НИКОЛАЕВНА', 'IssueDate': '01.03.2013', 'IssuerOrganization': 'ФМС77207',
                'IssuerOrganizationTranslit': 'FMS77207', 'LastNameRus': 'ВЯЛЬЦЕВА', 'PlaceOfBirthCity': 'МОСКОВСКАЯ ОБЛ.',
                'PlaceOfBirthCityTranslit': 'MOSKOVSKAJA OBL.', 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response4(self):
        google_response = "В РОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nМУИС\nТЕЛИ\nR2\nПОДПИСЬ ВЛАДЕЛЬЦА И\nHOLDER'S SIGNATURE\nВЫДАЧИ\nISSUING STATE\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nКОД ГОСУДАРСТВА/CODE OF\nТИП / TYPE\nНОМЕР ПАСПОРТА 9ASSPORT NO.\nПАСПОРТ /PASSPORT\nSESSING STATE 75 0097643\nRUS\nФАМИЛИЯ/SURNAME\nМАЖАРОВА /\nMAZHAROVA\nИМЯ/ GIVEN NAMES\nДАРЬЯ АНДРЕЕВНА /\nDARIA\nГРАЖДАНСТВО/NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/ RUSSIAN FEDERATION\nУЧЕТНАЯ ЗАПИСЬ\nДАТА РОЖДЕНИЯ / DATE OF BIRTH\n01.08.1996\nПОЛ /SEX МЕСТО РОЖДЕНИЯ /PLACE OF BIRTH\nЖ/F Г. МОСКВА / RUSSIA\nОРГАН, ВЫДАВШИЙ ДОКУМЕНТ / AUTHORITY\nДАТА ВЫДАЧИ / DATE OF ISSUE\nФМС 77117\n18.06.2014\nДАТА ОКОНЧАНИЯ СРОКА / DATE OF EXPIRY\nПОДПИСЬ ВЛАДЕЛЬЦА / HOLDER'S SIGNATURE\nДЕЙСТВИЯ\n18.06.2024\nMARTS\nPKRUS MAZHAROVA<<DARIA<<<<<<<<<<<<<<<<<<<<<<<\n7500976435 RUS 9608018F2406189<<<<<<<<<<<<<<04"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'ДАРЬЯ АНДРЕЕВНА', 'IssueDate': '18.06.2014', 'IssuerOrganization': 'ФМС77117',
                'IssuerOrganizationTranslit': 'FMS77117', 'LastNameRus': 'МАЖАРОВА', 'PlaceOfBirthCity': 'МОСКВА',
                'PlaceOfBirthCityTranslit': 'MOSKVA', 'PlaceOfBirthCountry': 'RUSSIA'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response5(self):
        google_response = "ИИ\nСА\n)\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nRUS\nПОДПИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\nШТИП\nТИПТІ ІТИ\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT\nТИП/TYPE - КОД ГОСУДАРСТВА/ CODE OF НОМЕР ПАСПОРТА / PASSPORT NO.\nВЫДАЧИ\n/ ISSUING STATE\nRUS\n75 0097643\nФАМИЛИЯ /SURNAME\nМАЖАРОВА /\nMAZHAROVA\nИМЯ/ GIVEN NAMES\nДАРЬЯ АНДРЕЕВНА /\nDARIA\nГРАЖДАНСТВО / NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/ RUSSIAN FEDERATION\nДАТА РОЖДЕНИЯ / DATE OF BIRTH\nУЧЕТНАЯ ЗАПИСЬ\n01.08.1996\nПОЛ/SEX МЕСТО РОЖДЕНИЯ /PLACE OF BIRTH\nЖ/\nF Г .МОСКВА / RUSSIA\nДАТА ВЫДАЧИ / DATE OF ISSUE\nОРГАН, ВЫДАВШИЙ ДОКУМЕНТ / AUTHORITY\n18.06.2014\nФМС 77117\nДАТА ОКОНЧАНИЯ СРОКА / DATE OF EXPIRY\nПОДПИСЬ ВЛАДЕЛЬЦА /HOLDER'S SIGNATURE\nДЕЙСТВИЯ\n18.06.2024\nMANO\nPKRUS MAZHAROVA<<DARIA<<<<<<<<<<<<<<<<<<<<<<<\n7500976435 RUS 9608018F2406189<<<<<<<<<<<<<<04"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'ДАРЬЯ АНДРЕЕВНА', 'IssueDate': '18.06.2014', 'IssuerOrganization': 'ФМС77117',
                'IssuerOrganizationTranslit': 'FMS77117', 'LastNameRus': 'МАЖАРОВА', 'PlaceOfBirthCity': 'МОСКВА',
                'PlaceOfBirthCityTranslit': 'MOSKVA', 'PlaceOfBirthCountry': 'RUSSIA'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response6(self):
        google_response = "РОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nПОДПИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\nRUS\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT\nТИП/TYPE КОД ГОСУДАРСТВА/CODE OF НОМЕР ПАСПОРТА /PASSPORT NO.\nВЫДАЧИ\nЅЅАNG ЅTАTЕ 75 8456866\nRUS\nESP\nФАМИЛИЯ/SURNAME\nМАВРОДИЙ /\nMAVRODIT\nИМЯ/GIVEN NAMES\nАРТУР АЛЕКСАНДРОВИЧ /\nARTUR\nГРАЖДАНСТВО /NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/RUSSIAN FEDERATION\nДАТА РОЖДЕНИЯ/DATE OF BIRTH\nУЧЕТНАЯ ЗАПИСЬ\n16.10.1989\nПОЛ/SEX\nМЕСТО РОЖДЕНИЯ /PLACE OF BIRTH\nM /M ЭСТОНИЯ / USSR\nДАТА ВЫДАЧИ / DATE OF ISSUE\nОРГАН, ВЫДАВШИЙ ДОКУМЕНТ / AUTHORITY\n12.07.2018\nМВД 50002\nДАТА ОКОНЧАНИЯ СРОКА /DATE OF EXPIRY\nПОДПИСЬ ВЛАДЕЛЬЦА/HOLDER'S SIGNATURE\nДЕЙСТВИЯ\n12.07.2028\nИДА 2\nPKRUS MAVRODII<<ARTUR<<<<<<<<<<<<<<<<<<<<<<<<\n7584 568661RUS 8910163М2 807122<<<<<<<<<<<<<<00\nАЛ\nУУ"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'АРТУР АЛЕКСАНДРОВИЧ', 'IssueDate': '12.07.2018', 'IssuerOrganization': 'МВД50002',
                'IssuerOrganizationTranslit': 'MVD50002', 'LastNameRus': 'МАВРОДИЙ', 'PlaceOfBirthCity': 'ЭСТОНИЯ',
                'PlaceOfBirthCityTranslit': 'ESTONIJA', 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response7(self):
        google_response = "РОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nАК\nАНТ\n,\n(RUS\nПОДПИСЬ ВЛАДЕЛЬЦА -\nHOLDER'S SIGNATURE\nW\nYRUS SALIVA\nISSUINC\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RU\nDERATION\nACNOPT/PASSPORT\nТИП / TYPE КОД ГОСУДАРСТВА/CODE O\nПІACRIOPТA /PASSPORT NO.\nВЫДАЧИ\n71 9389253\nФАМИЛИЯ / SURNAME\nЮНЕВ /\nYUNEV\nИМЯ /GIVEN NAMES\nАЛЕКСАНДР ВЛАДИМИРОВИЧ\nALEXANDER\nГРАЖДАНСТВО/NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN PATION\nДАТА РОЖДЕНИЯ /DATE OF BIRTH\nНАЯ ЗАПИСЬ\n02.12.1975\nПОЛ/SEX\nМЕСТО РОЖДЕНИЯ /PLACE OF BIRTH\nМ/М СМОЛЕНСКАЯ ОБЛ. / USSR\nДАТА ВЫДАЧИ / DATE OF ISSUE\nОРГАН, ВЫДАВШИЙ ДОКУМЕНТ / AUTHORITY\n25.05.2012\nФМС 77910\nДАТА ОКОНЧАНИЯ СРОКА /DATE OF EXPIRY\nПОДПИСЬ ВЛАДЕЛЬЦА /HOLDERS SIGNATURE\nДЕЙСТВИЯ\n25.05.2022\n50 %\nPKRUS YUNEV<<ALEXANDER<<<<<<<<<<<<<<<<<<<<<<<\n7193892537 RUS751202 1М2205256<<<<<<<<<<<<<<08"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'АЛЕКСАНДР ВЛАДИМИРОВИЧ', 'IssueDate': '25.05.2012', 'IssuerOrganization': 'ФМС77910',
                'IssuerOrganizationTranslit': 'FMS77910', 'LastNameRus': 'ЮНЕВ', 'PlaceOfBirthCity': 'СМОЛЕНСКАЯ ОБЛ.',
                'PlaceOfBirthCityTranslit': 'SMOLENSKAJA OBL.', 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response8(self):
        google_response = "I!!!\nРИМИ\nТУХАММЕН\nMINI\nІ\nКОНТРОЛИ!\nІНФОРМА И\nКАМИ\nІШІМЕТ\nҮШІНШІ\n50,\nКОМУ\nЗ\nULLO\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATIONS\nП\n2\nНАУЛЫ МИНИМУМ ЕДИН\nПРИНУДИ ТРИМА\nЛІТИН\nНАУКИ\nОТАНІТНІТИНИ.\nКИКИМИНАЛЬНУ І\nІНСІПІРУСУНУНУН ЖАНА\nРИ\nНЕМЕСТР\nRUS\nПОД НАШИТЕ\nНА ВАЈАРА В\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nГЕРБІЦІОНІ І\nEASKA 71 1855945\nCANADA\nСУСЕЙНОВ И\nGUSEYNOV\nТОА Е\nЭШГИНГИМДАГОГТЫ 1\nESHGIN -\nРЕАЛЕН\nPOCORWICKAN DAERALDIN RUSSIAN FEDERATION\nАКО\nRO AGE.\n04.01.1993\nIFHUN\nММ ГРУЗИЯ / GEORGIA\nНTA SAR REAT\nУ ПА АКО НЕ /АЛУ\n01.09.2010\nФМС 777071\nА ТАНИН НЬ БЬ И У\nПISIRLIGINIA BEYA\n01.09.2020\nP<RUSGUSEYNOY<<ESHG IN<<<<<<<<<<<<<<<<<<<<<<<\n71 185594 59RUS9301043M2009018<<<<<<<<<<<<<04"
        final_dict, data_array = parse_response(google_response)
        resp = {'IssuerOrganization': 'ФМС777071', 'IssuerOrganizationTranslit': 'FMS777071', 'PlaceOfBirthCityTranslit': '',
                'PlaceOfBirthCountry': 'GEORGIA'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response9(self):
        google_response = "РОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nRUS\nПОДПИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT ТИП / ТУРИ КОД ГАСУЛ ИРЕТНА/CODE OF НОМЕР ПАСПОРТА/PASSPORT NO.\nVISSUING STATE\nRUS\nНЕПАЧИТЕ\n6344676\nФАМИЛИЯ /SURNAME\nКОЛЕСНИКОВА /\nKOLESNIKOVA\nGEVEN NAMES\nЭЛЬВИРА НАДИРОВНА /\nELVIRA\nГРАЖДАНСТВО НАТОП LITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nДАТА РОЖДЕНИЯ;DATE OF BIRTH\nУЧЕТНАЯ ЗАПИСЬ\n20.04.2000\nПОЛ /SEX МЕСТО РОЖДЕНИЯ PLACE OF BIRTH\n Г. ЛИПЕЦК / RUSSIA\nДАТА ВОДИЧИ / DATE T O\nОРГАН, НАД ПИШИТИ ДОКУМЕНТ / AUTHORITY\n05.10.2011\nФМС 48001\nДАТА ОКОНЧАНИЯ СРОКА BUTE OF EXPRY\nПОДПИСЬ ВЛАДЕЛЬЦА/HOLDER'S SIGNATURE\nДЕЙСТВИЯ\n05.10.2021\nPKRUSKOLESNIKOVA<<ELVIRA<<<<<<<<<<<<<<<<<<<\n7163446764 RUSO004 204 F21 10053<<<<<<<<<<<<<<08"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'ЭЛЬВИРА НАДИРОВНА', 'IssuerOrganization': 'ФМС48001',
                'IssuerOrganizationTranslit': 'FMS48001', 'LastNameRus': 'КОЛЕСНИКОВА', 'PlaceOfBirthCity': 'ЛИПЕЦК',
                'PlaceOfBirthCityTranslit': 'LIPETSK', 'PlaceOfBirthCountry': 'RUSSIA'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response10(self):
        google_response = "КІРІ АРНА\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nУЛ\nI RUS\nПОДПИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\nРОССИЙСКАЯ ФЕДЕРАЦИЯ /RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT TUN/TYPE КОД ГОСУДАРСТВА/CODE OF НОМЕР ПАСПОРТА/PASSPORT NO.\n7 UING STATE 73 6153266\nР\nRUS\nФАМИЛИЯ / SURNAME\nЧЕРВИНСКАЯ І\nCHERVINSKAIA\nWE GIVEN NAMES\nЛИДИЯ ВЛАДИМИРОВНА /\nLIDITA\nГРАЖДАНСТВО /NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nДАТА РОЖДЕН /DATE OF BIRTH\nУЧЕТНАЯ ЗАПИСЬ\n21.11.1983\nПОЛ /SEX МЕСТО РОЖДЕНИЯ / PLACE OF BIRTH\nK/F КРАСНОЯРСКИЙ КРАЙ / USSR\nДАТА ВЫДАЧИ /DATE OF THE\nОРГАН, ВЫДАВШИЯ ДОКУМЕНТ/AUTHORITY\n01.10.2014\nФМС 24009\nДАТА ОКОНЧАНИЯ СРОКА ONTE OF EXPIRY\nПОДПИСЬ ИЛ ДЕЛЬВА/HOLDERS AGNATURE\nДЕЙСТВИЯ\n01.10.2024\nP<RUS CHERVINSKAIA<<LIDIIA<<<<<<<<<<<<<<<<<<<\n7361532667 RUS 831 121OF2410018<<<<<<<<<<<<<<06"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'ЛИДИЯ ВЛАДИМИРОВНА', 'IssuerOrganization': 'ФМС24009',
                'IssuerOrganizationTranslit': 'FMS24009', 'LastNameRus': 'ЧЕРВИНСКАЯ', 'PlaceOfBirthCity': 'КРАСНОЯРСКИЙ КРАЙ',
                'PlaceOfBirthCityTranslit': 'KRASNOJARSKIJ KRAJ', 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response11(self):
        google_response = "ПРИ\n1.\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nRUS\n- ПОДИТИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\n1. NЛ\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT TUN/TYPE КОД ГОСУДАРСТВА/CODE OF НОМЕР ПИCПOPТA/PASSPORT NO.\nНЬ ДАЧИ\nBING STATE .\nP\nRUS\n72 7590537\nФАМИЛИЯ / SURRIAME\nБЛИНОВА /\nBLINOVA\nИU GIVENAMES\nОЛЬГА АЛЕКСАНДРОВНА /\nOLGA\nГРИЛСТВО, МАСАN ALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nДАТА РОКЛЯ DE OF ORTH\nУЧЕТНАЯ ЗАПИСЬ\n20.07.1970\nNON/SEX MECTO POW PLACE OF BIRTH\nЖ/E СТАВРОПОЛЬСКИЙ КРАЙ / USSR\nДАТА ВЫДНИ DATE OF\nОРМАН, ИЫЛ ЗНШИЙ ДОКУМЕНТ/AUTHORITY\n12.02.2014\nФМС 77718\nДАRЕ ОКОНЧАНИЯ СРОКА PLE OF EXPRY\nПАПИСЬ ВЛАДЕЛЬШHOLDER'S ALARATURE\nДЕСТВЕ\n12.02.2024\nP<RUS BLINOVA<<OLGA<<<<<<<<<<<<<<<<<<<<<<<<<<\n7275905375 RUS7007204 F2402125<<<<<<<<<<<<<<06"
        final_dict, data_array = parse_response(google_response)
        resp = {'LastNameRus': 'БЛИНОВА', 'FirstNameFatherNameRus': 'ОЛЬГА АЛЕКСАНДРОВНА', 'IssuerOrganization': 'ФМС77718',
                'IssuerOrganizationTranslit': 'FMS77718', 'PlaceOfBirthCity': 'СТАВРОПОЛЬСКИЙ КРАЙ',
                'PlaceOfBirthCityTranslit': "STAVROPOL'SKIJ KRAJ", 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response12(self):
        google_response = "САНАЛ\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nRUS\nSP\nПОДПИСЬ ВЛАДЕЛЬЦА Е\nHOLDER'S SIGNATURE\nРОССИЙСКАЯ ФЕДЕРАЦИЯ / RUSSIAN FEDERATION\nПАСПОРТ / PASSPORT ТИП/ТУРО КОД ГОСУДАРСТВА/CODE OF ... НЕДАР ИСЛОТА/PASSPORT NO.\nTUN/ TYPE\nKORROSA POR ISSUING STATE 760865005\nФАМИЛИЯ /SURNAME\nГАЛКИНА ГО\nGALKINA\nИМЯ /GIVEN NAMES\nЕКАТЕРИНА ВЯЧЕСЛАВОВНА /\nEKATERINA\nГРАЖДАНСТВО/NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/RUSSIAN FEDERATION\nУЧЕТНАЯ ЗАПИСЬ\nДАТА РОЖДЕНИЯ /DATE OF BIRTH\n30.04.1969\nПОN/SEX МЕСТО РОЖДЕНИЯ/PLACE OT BIRTH\nМОСКОВСКАЯ ОБЛ. /USSR\nДАТА ВЫДАЧИ/DATE OF ISSUE\nОРГАН, ВЫДАНШИЙ ДОКУМЕНТ/AUTHORITY\n13.06.2019\nМВД 77713\nДАТА ОКОНЧАНИЯ СРОКА /DATE OF EXPIRY\nПОДПИСЬ ДЕЛА /HOLDER'S SIGNATURE\nДЕЙСТВИЯ\n13.06.2029\n/E\nPKRUSGALKINA<<EKATERINA<<<<<<<<<<<<<<<<<<<<<\n760865005 1 RUS 6904306F2906139<<<<<<<<<<<<<<04"
        final_dict, data_array = parse_response(google_response)
        resp = {'FirstNameFatherNameRus': 'ЕКАТЕРИНА ВЯЧЕСЛАВОВНА', 'IssueDate': '13.06.2019',
                'IssuerOrganization': 'МВД77713', 'IssuerOrganizationTranslit': 'MVD77713',
                'LastNameRus': 'ГАЛКИНА', 'PlaceOfBirthCity': 'МОСКОВСКАЯ ОБЛ.',
                'PlaceOfBirthCityTranslit': 'MOSKOVSKAJA OBL.', 'PlaceOfBirthCountry': 'USSR'}
        self.assertEqual(final_dict, resp)

    def test__parse_google_response13(self):
        google_response = "СА КАК\nVINNINUNONIS\nРОССИЙСКАЯ ФЕДЕРАЦИЯ\nRUSSIAN FEDERATION\nRUS\nПОДПИСЬ ВЛАДЕЛЬЦА\nHOLDER'S SIGNATURE\nРОССИЙСКАЯ ФЕДЕРАЦИЯ /RUSSIAN FEDERATION\nПАСПОРТ /PASSPORT TUN/TYPE КОД ГОСУДАРСТВА/CODE OF НОМЕР ПАСПОРТА /PASSPORT NO.\nВНАЧИН\nRUS\n7 НАЗВАЛИТР STATE 76 0449102\nФАМИЛИЯ/SURNAME\nОЛЕШКЕВИЧ !\nOLESHKEVICH\nИ СП ПАН\nВЛАДИМИР ЮРЬЕВИЧ І\nVLADIMIR\nГРАДИНС. TO NATIONALITY\nРОССИЙСКАЯ ФЕДЕРАЦИЯ/ RUSSSIAN FEDERATION\nДАТА РЕАЛНИ / DETS OF ORTH\nУМЕТНАЯ ПИСЬ\n17.03.2010\nNON/SEX\nМЕСТО РОКЛИ PICE OF BIRTH\n ГОР КРАСНОЯРСК / RUSSIA\nДАТА ВЬД ЧИ /DITE OF\nОРГАН, И ОПШТИ ДОКУМЕНТ/AUTHORITY\n11.04.2019\nМВД 50066\nДЛТА ОКОНЧЕН СРОКА TЕ ОF ЕXРМУ\nПОДПИСЫ ВЛАДЕЛЬЦА/HOLDER'S SIGNATURA\nДЕНСТВИЯ\n11.04.2029\nP<RUSOLESHKEVICH«<VLADIMIR<<<<<<<<<<<<<<<<<<\n76044 91025 RUS 1003178М2904 113<<<<<<<<<<<<<<08"
        final_dict, data_array = parse_response(google_response)
        resp = {'IssuerOrganization': 'МВД50066', 'IssuerOrganizationTranslit': 'MVD50066',
                'LastNameRus': 'ОЛЕШКЕВИЧ', 'PlaceOfBirthCity': 'ГОР КРАСНОЯРСК',
                'PlaceOfBirthCityTranslit': 'GOR KRASNOJARSK', 'PlaceOfBirthCountry': 'RUSSIA'}
        self.assertEqual(final_dict, resp)
