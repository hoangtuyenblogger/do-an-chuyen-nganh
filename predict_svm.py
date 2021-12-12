from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import time
import os
from sklearn.preprocessing import LabelEncoder
from Craw_Prossesing_Extract import text_prossesing
import pickle
from Craw_Prossesing_Extract import *
from pickle import dump

def Predict(url_news):
    # Chia tập train/test
    test_percent = 0.2 # train 8, test 2

    text = []
    label = []

    for line in open('news_categories.prep', encoding="utf-8"):
        words = line.strip().split()
        label.append(words[0])
        text.append(' '.join(words[1:]))

    X_train, X_test, y_train, y_test = train_test_split(text, label, test_size=test_percent, random_state=42)

    # encode label
    from sklearn.preprocessing import LabelEncoder
    label_encoder = LabelEncoder()
    label_encoder.fit(y_train)
    #print(list(label_encoder.classes_), '\n')
    y_train = label_encoder.transform(y_train)
    y_test = label_encoder.transform(y_test)

    MODEL_PATH = "models"
    dump(label_encoder, open(os.path.join(MODEL_PATH,"label_encoder.pkl"), 'wb'))

    #load model

    model = pickle.load(open(os.path.join(MODEL_PATH,"svm_model.pkl"), 'rb'))


    title, des,key, text = get_data_news(url_news)
    label = model.predict([text])
    return label_encoder.inverse_transform(label)

def news_predict(url):
    # load model
    MODEL_PATH = "models"
    model = pickle.load(open(os.path.join(MODEL_PATH, "svm_model.pkl"), 'rb'))

    label_encoder = pickle.load(open(os.path.join(MODEL_PATH, "label_encoder.pkl"), 'rb'))

    title, des, key, text = get_data_news(url)
    label = model.predict([text])
    return label_encoder.inverse_transform(label)

if __name__ == '__main__':
    while True:
        url_news = input("Nhập link báo: ")
        print(news_predict(url_news))