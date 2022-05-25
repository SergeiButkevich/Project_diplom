import requests
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
    """
    Function to get html.
    url: We will pass the url to the first parameter.
    params: In the second, the parameters themselves are directly or if they are not, we will fill the void.
    return: at the end of the function will return an object with html.
    """
    r = requests.get(url, headers=Headers, params=params)
    return r


def get_content(html):
    """
    We will paste the already received html into this function.
    soup: Helps parse html and get the information we need.
    items: We will look specifically for the blocks of interest to us.
    iPhones: We will put the goods that interest us here.
    return: The function will return our iPhones list.
    """
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


def result(items, walk):
    """
    The function will take 2 parameters, what we want to save is items and the path where we want to save is walk.
    wich open: Open the file and skip the path and specify the format for writing.
    writer: We assign this transom data for further work with CSV. The first parameter is the file, the second separator.
    writer.writerow: call this method to set the string (headers).
    At the end, we start a cycle to write data.
    """
    with open(walk, "w", newline="", encoding="cp1251", errors="ignore") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Описание", "Ссылка"])
        for item in items:
            writer.writerow([item["Описание"], item["Ссылка"]])


def parser():
    """
    The function will receive the html object and write it somewhere.
    html: Variable to get the html object with its entry. As a parameter, we pass our url.
    PAGENATION - Constant to specify the number of pages to parse.
    In the if statement, we check the response code to make sure that our site is working.
    """
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
