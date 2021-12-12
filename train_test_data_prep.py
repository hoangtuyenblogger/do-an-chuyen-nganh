import numpy as np
import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import time

#########################
# Chia tập train/test
test_percent = 0.2 # train 8, test 2

text = []
label = []

for line in open('news_categories.prep', encoding="utf-8"):
    words = line.strip().split()
    label.append(words[0])
    text.append(' '.join(words[1:]))

X_train, X_test, y_train, y_test = train_test_split(text, label, test_size=test_percent, random_state=42)

# Lưu train/test data
# Giữ nguyên train/test để về sau so sánh các mô hình cho công bằng
with open('train.txt', 'w', encoding="utf-8") as fp:
    for x, y in zip(X_train, y_train):
        fp.write('{} {}\n'.format(y, x))

with open('test.txt', 'w', encoding="utf-8") as fp:
    for x, y in zip(X_test, y_test):
        fp.write('{} {}\n'.format(y, x))

# encode label
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
#print(list(label_encoder.classes_), '\n')
y_train = label_encoder.transform(y_train)
y_test = label_encoder.transform(y_test)

########################################## SVM training
from sklearn.svm import SVC

start_time = time.time()
text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1,1),max_df=0.8)),
                     ('tfidf', TfidfTransformer()),('clf', SVC(gamma='scale'))
                    ])

text_clf = text_clf.fit(X_train, y_train)

train_time = time.time() - start_time
print('Training xong, time = ', train_time, 's')
########################################## tạo thư mục lưu model
MODEL_PATH = "models"

import os
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)
# Save model
pickle.dump(text_clf, open(os.path.join(MODEL_PATH, "svm_model.pkl"), 'wb'))

# SVM Accuracy
model = pickle.load(open(os.path.join(MODEL_PATH,"svm.pkl"), 'rb'))
y_pred = model.predict(X_test)
print('SVM, Accuracy =', np.mean(y_pred == y_test))
