from bs4 import BeautifulSoup
import glob
import os
import requests
import wget


mipt0 = "https://mipt.ru"
mipt_scedule = "https://mipt.ru/about/departments/uchebniy/schedule/study"


request = requests.get(mipt_scedule)
html = BeautifulSoup(request.content, "html.parser")


def update_excels():
    for file in glob.glob("excels/*"):
        os.remove(file)
    for tag in html.find_all('a', href=True):
        if tag['href'][0:20] == "/upload/medialibrary":
            wget.download(mipt0 + tag['href'], "excels")
    print()
    print("Расписание обновлено!")
