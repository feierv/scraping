from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import date


def results(request):
    # capabilities = dict(DesiredCapabilities.CHROME)
    # capabilities['proxy'] = {'proxyType': 'MANUAL','httpProxy': '3.95.61.16','ftpProxy': '3.95.61.16','sslProxy': '3.95.61.16','noProxy': '',
    # 'class': "org.openqa.selenium.Proxy",'autodetect': False}
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--verbose')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-software-rasterizer')
    # chrome_options.add_argument('--headless')
    # options=chrome_options)
    # import requests

    # proxies = {"http": "http://10.10.1.10:3128",        
    #        "https": "http://10.10.1.10:1080"}

    # requests.get("http://example.org", proxies=proxies)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    results = []

    for page_num in range(1, 12):
        driver.get(f"https://stackoverflow.com/jobs/companies/?pg={page_num}")
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        page = soup.find_all('div', attrs={'class':'dismissable-company'})
        from pprint import pp
        for d in page:
            name = d.find('a', attrs={'class':'s-link'}).next_element
            name = name[:-1] if name[-1] == ' ' else name
            name = name.replace(' ', '-').replace('-&', '').replace('.', '').replace('--', '-')
            driver.get("https://stackoverflow.com/jobs/companies"+f"/{name}")
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
            page = soup.find('div', attrs={'class':'ba bc-black-100 ps-relative p16 bar-sm'})
            if page:
                value = page.find('div', attrs={'class': 'd-flex flex__fl-grow1 mt12'}).find('span').next_element
                employees_value = value.replace(' ', '').replace('employees', ' employees').replace('\n', '')
                data = dict()
                data['business_name'] = name
                data['number_of_employees'] = employees_value
                categories = page.find('div', attrs={'class': 'mt12'}).find('span').next_element
                categories = categories.replace(' ', '').replace('\n', '')
                data['industries'] = categories
                site = page.find('a')
                data['website'] = str(site['href'])
                years_in_business = page.find('div', attrs={'class': 'd-flex flex__fl-grow1 mt12'}).find_all('span')[1].next_element
                years_in_business = years_in_business.replace(' ', '').replace('\n', '')
                current_year = date.today().year
                try:
                    years_in_business = current_year - int(years_in_business)
                    data['years_in_business'] = years_in_business
                    results.append(data)
                except ValueError:
                    data['years_in_business'] = 'private'

    driver.quit()
    return HttpResponse(results)