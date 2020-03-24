import json
import requests
from bs4 import BeautifulSoup

url_base = "https://listado.mercadolibre.com.co/xiaomi"
print('Start scraping xiaomi')
data = {}
try:
    get_response = requests.get(url_base)
    html = BeautifulSoup(get_response.content, 'html.parser')
    products = html.find_all('li', {'class': 'results-item highlighted article stack product'})

    for prod in products:
        id_prod = prod.find('div', {'class': 'rowItem'}).get('id')
        title = prod.find('span', {'class': 'main-title'}).text
        price = prod.find('span', {'class': 'price__fraction'}).text.replace('.', '')
        url_prod = prod.find('a', {'class': 'item__info-title'}).get('href')
        images = []
        for img in prod.find_all('img'):
            if img.get('src'):
                images.append(img.get('src'))
            else:
                images.append(img.get('data-src'))

        data_prod = {
            "id": id_prod,
            "title": title,
            "price": price,
            "url": url_prod,
            "images": images
        }
        data[id_prod] = data_prod
    f = open('data.json', 'w')
    f.write(json.dumps(data))
    f.close()
    print('finish....')
except requests.exceptions.RequestException as e:
    print(str(e))
