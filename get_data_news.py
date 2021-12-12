import newspaper
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import sqlite3


#url = "https://dantri.com.vn/xa-hoi/thu-tuong-yeu-cau-tiep-tuc-kiem-soat-nguoi-ra-vao-tphcm-20210930183408003.htm"

'''print(article.title)
print(article.text)
print(article.top_img)'''


#print(category)

#print(article.meta_keywords)

'''conn = sqlite3.connect("data.db")
query ='INSERT INTO data_news (title,description,content,keywords,url_news,url_img) VALUES (?,?,?,?,?,?)'
conn.execute(query, (article.title,article.meta_description,article.text,keywords,article.url,article.top_img))
conn.commit()
print("Done ",url)'''


def get_data_news(url, conn):
    try:
        article = Article(url)
        article.download()
        article.parse()

        keywords = ''
        for keyword in article.meta_keywords:
            keywords = keywords + keyword + '|'
        # print(keywords)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        category_element = soup.find('ul', class_="dt-breadcrumb")
        li_element = category_element.findAll('li')
        category = li_element[-1].text.strip()

        # conn = sqlite3.connect("data.db")
        query = 'INSERT INTO data_news (title,description,content,keywords,url_news,url_img) VALUES (?,?,?,?,?,?)'
        conn.execute(query,
                     (article.title, article.meta_description, article.text, keywords, article.url, article.top_img))
        conn.commit()
        print("Done ", url)
    except Exception as erro:
        print(print("Đã có lỗi:", erro))
        pass

if __name__ == '__main__':
    try:
        conn = sqlite3.connect("data.db")

        print("######## Cào dữ liệu theo thứ tự ID bài báo")
        start = int(input("Bắt đầu từ: "))
        end = int(input("Đến: "))
        link_news = conn.execute("SELECT id, link FROM links_news where id BETWEEN ? AND ?", (start, end))

        for row in link_news:
            get_data_news(row[1], conn)
    except Exception as erro:
        print("Đã có lỗi:", erro)
        pass