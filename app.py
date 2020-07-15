from flask import Flask, render_template,request, Response
import pickle
import os, string, re
import pandas as pd
import numpy as np


CON_FOLDER = os.path.join('static', 'confusion_matrix')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = CON_FOLDER


@app.route("/")
def home():
    return render_template("trangchu.html")

@app.route("/home")
def home2():
    return render_template("trangchu.html")

@app.route("/thongtinsanpham")
def thongtinsanpham():
    return render_template("thongtinsanpham.html")


@app.route("/thongtindulieu")
def thongtindulieu():
    return render_template("thongtindulieu.html")


@app.route("/uploadFiledudoan")
def uploadFiledudoan():
    return render_template("Nhapfile.html")

@app.route("/ketquathinghiem")
def ketquathinghiem():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'confusemaxtrix.png')
    return render_template("ketquathinghiem.html",conf_image = full_filename)


@app.route("/predict/", methods=['POST'])
def classify_text():
    try:
        value1 = request.form['msg1']
        value2 = request.form['msg2']
        value3 = request.form['msg3']
        value4 = request.form['msg4']
        value5 = request.form['msg5']
        value6 = request.form['msg6']
        value7 = request.form['msg7']
        value8 = request.form['msg8']
        print(value1,value2,value3,value4,value5,value6,value7)

        x_test = [float(value1),float(value2),float(value3),float(value4),float(value5),float(value6),float(value7),float(value8)]
        x_test = np.asarray(x_test)

        filename = 'KNN.pickle'
        classifier = pickle.load(open(filename, 'rb'))
        y_pred = classifier.predict([x_test])
        if int(y_pred) == 1:
            label = "RÂT TIẾC, BẠN ĐÃ CÓ DẤU HIỆU BỆNH TIỂU ĐƯỜNG"
        else:
            label = "CHÚC MỪNG BẠN, SỨC KHỎE CỦA BẠN BÌNH THƯỜNG"

        return render_template("ketquadudoan.html", data = [{"label":label}])
    except:
        label = "XIN LỖI, VUI LÒNG NHẬP ĐẦY ĐỦ CÁC THÔNG TIN"
        return render_template("ketquadudoan.html", data = [{"label":label}])


filename = 'KNN.pickle'
classifier = pickle.load(open(filename, 'rb'))

@app.route("/ketquadudoanFile", methods=['POST'])
def ketquadudoanFile():
    if request.method == 'POST':
        fileupload = request.files['file']
        try:
            data = pd.read_csv(fileupload) 
            data.fillna(0.0)
            print(data.head())
            try:
                X_test = data.drop('Outcome', 1)
            except:
                X_test = data
            predict_list = classifier.predict(X_test)
            output_predict = []
            for re in predict_list:
                output_predict.append(re)
            X_test["Dự đoán"]=output_predict
            X_test['Dự đoán'] = X_test['Dự đoán'].map({1: 'Tiểu Đường', 0: 'Bình Thường'})
            print(X_test.head())
            X_test.to_csv('uploads/result.csv', index = False, header=True)
            return render_template('ketquanhapFile.html',  tables=[X_test.to_html(classes='data')], titles=X_test.columns.values)
        except:
            label = "XIN LỖI, VUI LÒNG NHẬP FILE ĐẦY ĐỦ THÔNG TIN"
            return render_template("Error_ketquanhapFile.html",data = [{"label":label}])

# Hàm xuất file
@app.route("/exportCSV")
def exportCSV():
    with open("uploads/result.csv",'r',encoding='utf-8') as fp:
         csv = fp.read()
    return Response( csv, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=result.csv"})
    

if __name__ == "__main__":
    app.run(debug=True)
