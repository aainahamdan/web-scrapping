from wsgiref import headers
import requests
import pandas as pd
from bs4 import BeautifulSoup


try:
    headers = {'User Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    url = 'https://www.listofcompaniesin.com/beauty-personal-care-in-malaysia.html'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    companies = soup.find('div', {'class' : 'body'}).find_all('ul')

    for item in companies:
        name = item.find('h4').a.text
        tel = item.find('p', {'class': 'low'}).span.text.strip('Telephone : ')
        address = item.find('span').text
        print(address)
        break

except Exception as e:
    print(e)