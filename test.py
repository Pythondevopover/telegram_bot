# import requests
# from bs4 import BeautifulSoup
# url = 'https://robocontest.uz/profile/sardor_630'
# with open("profil3.html", "w", encoding="utf-8") as f:
#     f.write(requests.get(url).text)
import requests
url = 'https://robocontest.uz/profile/'
print(requests.get(url + '1-yj').status_code)