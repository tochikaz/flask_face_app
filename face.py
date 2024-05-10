import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
import numpy as np


classes = ['happy','angry']
image_size = 48

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSION = 'jpg'

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

model = load_model('./model.h5', compile= False)#学習済みモデルをロード

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print('upload file')
    print(request.method)
    if request.method == 'POST':
        if 'file' not in request.files:
            print('if_1')
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        print(allowed_file(file.filename))
        print(file.filename)
        if file.filename == '':
            print('if_2')
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print('if_3')
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換
            img = image.load_img(filepath, target_size=(image_size,image_size))
            img = image.img_to_array(img)
            data = np.array([img])
            #変換したデータをモデルに渡して予測する
            result = model.predict(data)[0]
            predicted = result.argmax()
            pred_answer = "これは " + classes[predicted] + " です"

            return render_template("index.html",answer=pred_answer)
        else :
            print('else')

    return render_template("index.html",answer="")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)