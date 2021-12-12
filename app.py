from tkinter import  *
from tkinter import messagebox
import pickle
import os
from Craw_Prossesing_Extract import get_data_news, extract_data

def news_predict(url):
    # load model
    MODEL_PATH = "models"
    model = pickle.load(open(os.path.join(MODEL_PATH, "svm_model.pkl"), 'rb'))

    label_encoder = pickle.load(open(os.path.join(MODEL_PATH, "label_encoder.pkl"), 'rb'))

    title, des, key, text = get_data_news(url)
    label = model.predict([text])

    print(list(label_encoder.classes_), '\n')
    return label_encoder.inverse_transform(label)


def predict():
    link_news = input_link_news.get("1.0",'end-1c')
    # xóa dữ liệu cũ
    input_title.delete("1.0",'end-1c')
    input_content.delete("1.0",'end-1c')
    input_keyword.delete("1.0",'end-1c')
    input_lable.delete("1.0",'end-1c')

    # lấy dữ liệu bài báo
    try:
        _title, _des, _keyword, _text = get_data_news(link_news)
        _sumaried_text, _key = extract_data(_text)
    except Exception as erro:
        reset()
        messagebox.showwarning("Cảnh báo", "Hãy nhập đúng đường dẫn!")

    # dự đoán nhãn bài báo
    lable_news = news_predict(link_news)

    # add dữ liệu lên form
    input_title.insert("1.0", _title)
    input_content.insert("1.0",_sumaried_text)
    input_keyword.insert("1.0", _keyword)
    input_lable.insert("1.0", lable_news)

    # không cho sửa textbox
    input_title.config(state='disabled')
    input_content.config(state='disabled')
    input_lable.config(state='disabled')
    input_keyword.config(state='disabled')

def reset():
    # đặt lại trạng thái enable cho textbox
    input_title.config(state='normal')
    input_content.config(state='normal')
    input_lable.config(state='normal')
    input_keyword.config(state='normal')

    # xóa dữ liệu cũ
    input_title.delete("1.0",'end-1c')
    input_link_news.delete("1.0",'end-1c')
    input_content.delete("1.0",'end-1c')
    input_keyword.delete("1.0",'end-1c')
    input_lable.delete("1.0",'end-1c')


    # focus vào textbox nhập link bài báo
    input_link_news.focus()

if __name__ == '__main__':
    app = Tk()
    app.resizable(False, False)
    app.geometry("1200x600")
    app.title("Demo đồ án cơ sở ngành")

    # nhập link bài báo
    lbl_link_news = Label(app, text="Nhập link báo vào bên dưới:", font=("Helvetica", 12))
    lbl_link_news.pack(pady=10, side= TOP, anchor="w")
    input_link_news = Text(app, height=1, width=100,font=("Helvetica", 12))
    input_link_news.pack()
    input_link_news.focus()

    # tiêu đề bài báo
    lbl_title = Label(app, text="Tiêu đề:", font=("Helvetica", 12))
    lbl_title.pack(pady=5, side= TOP, anchor="w")
    input_title = Text(app, height=1, width=100,font=("Helvetica", 12))
    input_title.pack()

    # nội dung tóm tắt bài báo
    lbl_content = Label(app, text="Nội dung tóm tắt:", font=("Helvetica", 12))
    lbl_content.pack(pady=5, side= TOP, anchor="w")
    input_content = Text(app, height=12, width=100,font=("Helvetica", 12))
    input_content.pack()

    # keyword bài báo
    lbl_keyword = Label(app, text="Keyword:", font=("Helvetica", 12))
    lbl_keyword.pack(pady=5, side= TOP, anchor="w")
    input_keyword = Text(app, height=2, width=100,font=("Helvetica", 12))
    input_keyword.pack()

    # nhãn bài báo
    lbl_lable = Label(app, text="Nhãn dự đoán:", font=("Helvetica", 12))
    lbl_lable.pack(pady=5, side= TOP, anchor="w")
    input_lable = Text(app, height=2, width=100,font=("Helvetica", 12))
    input_lable.pack()


    # button dự đoán
    btn_predict = Button(app,height=1, width=10, text="Dự đoán", command=predict)
    btn_predict.pack()

    # button reset
    btn_reset = Button(app,height=1, width=10, text="Reset", command=reset)
    btn_reset.pack()

    app.mainloop()
