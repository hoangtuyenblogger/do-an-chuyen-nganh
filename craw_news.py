from newspaper import Article
import re
import warnings

import requests
from bs4 import BeautifulSoup
from gensim.summarization import keywords as get_keywords
from gensim.summarization import summarize
from newspaper import Article
from pyvi.ViTokenizer import tokenize

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')



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


def get_data_news(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        meta_description = article.meta_description
        meta_description = " ".join(meta_description.split())

        text = article.text

        # get keywword
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        category_element = soup.find('ul', class_="dt-news__tag-list")
        a_element = category_element.findAll('a')
        keyword = [a.text for a in a_element]

        return article.title, meta_description, keyword, text

    except Exception as erro:
        print(print("Đã có lỗi:", erro))
        pass

def text_prossesing(text):
    text = re.sub(r'\s\s+', ' ', text.strip())
    # load stopword
    stopwords_vietnam = []
    with open('stopword_vietnam.txt', 'r', encoding="utf8") as f:
        for line in f:
            stopwords_vietnam.append(line.strip())

    # lowercase
    text = text.lower()

    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

    # remove stopword
    text = ' '.join([word for word in text.split() if word not in stopwords_vietnam])

    text = tokenize(text)

    return text
def extract_data(text_processed, ratio=0.2):
    return summarize(text, ratio=0.2), get_keywords(text, ratio=0.2)

if __name__ == '__main__':
    #url= "https://dantri.com.vn/giao-duc-huong-nghiep/hoc-sinh-tu-vong-do-dien-thoai-no-khi-hoc-truc-tuyen-bo-giao-duc-noi-gi-20211015122857839.htm"
    url = input("Nhập link bài báo: ")
    title, des,key, text = get_data_news(url)

    print("Origin text: ",text)
    print("===================================================")
    print("Description: ", des)
    print("===================================================")
    print("keyword from news: ",key )
    text = text_prossesing(text)
    print("text clean: ",text)
    print("===================================================")
    print("summarized:", summarize(text, ratio=0.2))
    print("===================================================")
    print("Keyword: ",get_keywords(text, ratio=0.1))