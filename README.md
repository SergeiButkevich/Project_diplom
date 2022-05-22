# Project_diplomimport requests
from bs4 import BeautifulSoup
import csv

CSV = "iPhones.csv"
HOST = "https://www.21vek.by/"
URL = "https://www.21vek.by/mobile/iphone_13/"

Headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                     "application/signed-exchange;v=b3;q=0.9",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                         "101.0.0.0 Safari/537.36"
           }


def get_html(url, params=""):
    r = requests.get(url, headers=Headers, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", class_="result__item")
    iPhones = []
    for item in items:
        iPhones.append(
            {
                "Описание": item.find("span", class_="result__name").get_text(strip=True),
                "Ссылка": item.find("a").get("href"),
            }
        )
    return iPhones


def result(items,walk):
    with open(walk, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Описание", "Ссылка"])
        for item in items:
            writer.writerow([item["Описание"], item["Ссылка"]])


def parser():
    PAGENATION = input("Тыкни лапкой колличество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        iPhones = []
        for page in range(1, PAGENATION):
            print(f"Я в процессе уже: {page}")
            html = get_html(URL)
            iPhones.extend(get_content(html.text))
            result(iPhones, CSV)
    else:
        print("Error")


parser()

