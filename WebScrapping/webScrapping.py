import requests
from bs4 import BeautifulSoup

URL = 'https://dps.usc.edu/category/alerts/'
page = requests.get(URL)
html = page.content
#print(html)

soup = BeautifulSoup(html, 'html.parser')
print(soup)