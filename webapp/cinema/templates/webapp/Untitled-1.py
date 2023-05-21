import bs4
import requests
data = requests.get('https://rezka.ag/?filter=watching').text
print(data)