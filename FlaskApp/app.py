# save this as app.py
from flask import Flask, request, jsonify
import os
import tensorflow as tf
import cv2 as cv
from PIL import Image
import numpy as np
import tensorflow as tf
import math
import collections



import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
model=tf.keras.models.load_model(r'D:\models-backup\intel\VGG16_scratch_150_0.88.h5')
classes = ['Buildings', 'Forest', 'Glaciers', 'Mountains', 'Sea', 'Street']

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@app.route("/")
def hello():
    return "Send post request to /upload with img file using postMan as key = inp_img to get prediction of class"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'inp_img' not in request.files:
            dictToReturn = {'inp_img_name': "No file is choosen"}
            return jsonify(dictToReturn)
        file = request.files['inp_img']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            dictToReturn = {'inp_img_name': "No file is choosen"}
            return jsonify(dictToReturn)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename) # file will be saved.
            
            img = cv.imread(filename)
            os.remove(filename)
            
            IMG_SIZE = (150,150) # for VGG16
            img = cv.resize(img,IMG_SIZE)
            img=img/255.0
            img = np.expand_dims(img, axis=0)
            predict_x= model.predict(img)

            li=[]
            for val in predict_x[0]:
                li.append(float(val)*100)

            dir_clases = dict(zip(li,classes))

            return jsonify(dir_clases)

if __name__ == "__main__":
    app.run(debug=True)