import requests
from bs4 import BeautifulSoup as bs


headers = {'accept' : '*/*',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
           'Connection':'keep-alive',
            'Cookie' : 'SID=qQfJJ0cX2GW9drD_GcrJrC2mX_cNRCJR3yVPCpIXqMxWUTqyTMi0HwG4isZcsT99_qFg0A.; '
                       'HSID=AEUzqkbnMfA7em7iR; SSID=Ax0WZ_tD9lM54jK9L; APISID=KTwXM3XLVtA3Qcfz/AUUqEGmJv50-boxhI; SAPISID=ekjWS-C1fbQ7yuTd/ASlTuIlDNMSwqqcwe; '
                       'NID=191=mCaLqN5K6IDuXj4a_xfgAxPon6gISvqUlvqeYNBGWK-S1ZOpYrZvKTbdSfEJ_DQeoMHLFwQj3ubCPAJyiND8fsaEBQb17deHCagBzntN8zD5G3WnexLa6Ajnt_xX59tk0OXkCTKDOoJd6Hf7f0vTToyLDGGJyGTEtu9RUOBPHUsrvglHQVDZ0_mT_AeUQK6AD_B_ERzStShLZAczdBb7lYafOMf9U7MplmWDVbLl; SIDCC=AN0-TYvwxVx3ahp_O5PAFtuyFjylWM3mvwhqKn4_FGbz_w7KKpKtKiMxfe0RVDzFXftiFsM36y8; 1P_JAR=2019-11-11-21; SEARCH_SAMESITE=CgQIo44B; ANID=AHWqTUl0HiPqOCE10GTWb-IOWBDowM4omXapZPqkUkmty1rIAg32-dkaGhTdSpd-; '
                       'DV=E3eLU7sh1tFGQAgxTl7ANXYQiKXG5RbWSxWyBWS9uAIAAGCtLueKQ3moKgEAAOw7mDvytuuRUgAAAA'
           }

base_url = 'https://auto.ru/moskva/cars/vendor-foreign/all/?year_from=2013&price_to=500000&km_age_to=100000&pts_status=1&transmission=ROBOT&transmission=AUTOMATIC&transmission=VARIATOR&transmission=AUTO&page=1'


def autoru_parse(base_url, headers):
    cars = []
    urls = [base_url]
    session = requests.session()
    request = session.get(base_url, headers = headers)
    if request.status_code == 200:
        try:
            soup = bs(request.content, 'lxml')
            pagination = soup.find_all('a', attrs = {'class' : 'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page'})
            total_pages = int(pagination[-1].text)
            for i in range(total_pages):
                url = f'https://auto.ru/moskva/cars/vendor-foreign/all/?year_from=2013&price_to=500000&km_age_to=100000&pts_status=1&transmission=ROBOT&transmission=AUTOMATIC&transmission=VARIATOR&transmission=AUTO&page={i+1}'
                if url not in urls:
                    urls.append(url)
        except:
            print('Something went wrong, probably there''s no pages to collect data from')
    for url in urls:
        request = session.get(url, headers = headers)
        soup = bs(request.content, 'lxml')

        divs = soup.find_all('div', attrs = {'class' : 'ListingItem-module__columnCellSummary'})
        print(divs)




autoru_parse(base_url, headers)
