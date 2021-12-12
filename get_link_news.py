from bs4 import BeautifulSoup
import requests
import csv
import sqlite3



def get_link_highlight_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    highlight_new_element = soup.find('div', class_="dt-highlight clearfix")
    h3_highlight_new_element = highlight_new_element.findAll('h3', class_="news-item__title")
    link_news = [h3.find('a').attrs['href'] for h3 in h3_highlight_new_element]
    # print(link_news)
    return link_news


def get_link_news_by_day(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    new_element = soup.findAll('div', class_="news-item news-item--timeline news-item--left2right")
    link_news = [div.find('a').attrs['href'] for div in new_element]
    return link_news


def add_data(data): #data là list chứa link vd: /suc-khoe/dai-dich-covid-19/3-9-2021.htm
    conn = sqlite3.connect("data.db")
    query = "INSERT INTO links_news(link) VALUES (?)"
    for link in data:
        full_link = "https://dantri.com.vn/" +link
        conn.execute(query, (full_link,))
        conn.commit()
        print("added to database ", full_link)


def get_link_news():
    try:
        url = input("Nhập link báo dân trí cần get: ")
        option = input("""Chọn bài cần get:
                                    1. Các bài nổi bật
                                    2. Các bài theo ngày
        """)
        if(option == 1):
            data = get_link_highlight_news(url)
            add_data(data)
        else:
            data = get_link_news_by_day(url)
            add_data(data)
    except Exception as erro:
        print("Đã có lỗi: ", erro)
        pass

if __name__ == '__main__':
    month = input("Nhập tháng cần get: ")
    day_start = input("Nhập ngày bắt đầu cần get: ")
    day_end = input("Cho đến ngày: ")

    for day in range(int(day_start),int(day_end)):
        url = "https://dantri.com.vn/suc-khoe/dai-dich-covid-19/{}-{}-2021.htm".format(str(day),str(month))
        print("Root url: ",url )
        print("====================================================================================")
        try:
            data = get_link_news_by_day(url)
            add_data(data)
        except Exception as erro:
            print("Đã có lỗi: ", erro)
            pass
