import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


headers = {'Accept': 'text/html, */*; q=0.01',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept-Encoding': 'gzip, deflate, br'
           }
base_url = 'https://www.1cbit.ru/contacts/'
api_key = 'paste_ur_api_key'
base_geo_url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode=Россия, '
data = 'action=city-load&idcitypopup=undefined&ui_prioritet=46,47&smart_redirect=N'
headers_url = 'https://www.1cbit.ru/bitrix/templates/.default/components/vitams/city.dropdown/city_popup/ajax.php'




def find_headers(headers_url, data, headers):
    r = requests.post(headers_url, data=data, headers=headers)
    # request = session.get(headers_url, headers=headers)
    if r.status_code == 200:
        datacodes = []
        soup = bs(r.content, 'lxml')
        a_tags = soup.find_all('a', attrs={'data-country-code': 'ru'})
        for a in a_tags:
            datacodes.append({
                'City': a.text,
                'code': a['data-code']})
    return datacodes


def bit_parse(headers, datacodes, city_names):
    res = []
    for code, name in zip(datacodes, city_names):
        session = requests.session()
        request = session.get(f'https://{code}.1cbit.ru/contacts/', headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            addresses = soup.find_all('div', attrs={'class': 'place'})
            for address in addresses:
                res.append({
                    'City': name,
                    'Address': address.text})
    return res


def make_frame_to_excel(writer, data):
    #data = pd.DataFrame(offices)
    data.to_excel(writer, sheet_name='Contacts', index=False)


def geocoding(data):
    data['Geocode'] = 'Not defined'
    for i in range(len(data['Address'])):
        request = requests.get(base_geo_url + data['City'][i] + data['Address'][i], headers=headers)
        soup = bs(request.content, 'lxml')
        try:
            data['Geocode'][i] = soup.find('pos').text
        except:
            pass
    return data


datacodes = find_headers(headers_url, data, headers)

city_code = []
city_names = []
for code in datacodes:
    city_code.append(list(code.values())[1])
    city_names.append(list(code.values())[0])

res = bit_parse(headers, city_code, city_names)

without_geo = pd.DataFrame(res)

geocode = geocoding(without_geo)

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

make_frame_to_excel(writer, geocode)

writer.save()
