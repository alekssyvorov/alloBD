import requests
from bs4 import BeautifulSoup
import lxml
import time
import sqlite3


connection = sqlite3.connect("products_sale.db", 5)
cur = connection.cursor()
# cur.execute("CREATE TABLE products (title TEXT, price TEXT);")

page = int(input('Input numbers page '))
session = requests.Session()
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

for i in range(1, page+1):
    url = f'https://allo.ua/ua/universalnye-mobilnye-batarei/p-{i}/'
    data_lst = []
    response = session.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    all_product = soup.find('div', class_='products-layout__container products-layout--grid')
    products = all_product.find_all('div', class_='product-card')
    for j in range(len(products)):
        try:
            price = products[j].find('div', class_='v-pb__cur discount')
            title = products[j].find('a', class_='product-card__title')
            data = title.text, price.text
            data_lst.append(data)
            print(title.text)
            print(price.text)
        except:
            print('Нет скидки')
    request_data = f"INSERT INTO products (title, price) VALUES (?, ?);"
    cur.executemany(request_data, data_lst)
    time.sleep(3)
    print(f'Page {i}')

connection.commit()
connection.close()


connection = sqlite3.connect("products_sale.db", 5)
cur = connection.cursor()
cur.execute("SELECT * FROM products;")
for row in cur:
    print(row)