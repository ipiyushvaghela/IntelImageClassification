import streamlit as st
import tensorflow as tf
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
import math
@st.cache(allow_output_mutation=True)
def load_model():
  model=tf.keras.models.load_model(r'..\IntelImageClassification\BestPerformingModels\VGG16_scratch_150_0.88.h5')
  return model


with st.spinner('Model is being loaded..'):
  model=load_model()

st.write("""
         # Intel Image Classification
         """
         )

file = st.file_uploader("Upload the image to be classified", type=["jpg", "png","jpeg"])


st.set_option('deprecation.showfileUploaderEncoding', False)
col1, col2 = st.columns(2)

if file is None:
    st.text("Please upload an image file")
else:
    with col1:
      image = np.array(Image.open(file))
      # IMG_SIZE = (331,331) # for NNL only
      IMG_SIZE = (150,150) # for VGG16
      img = cv2.resize(image,IMG_SIZE)
      img=img/255.0
      img = np.expand_dims(img, axis=0)
      st.image(img,width = 300)
      predict_x= model.predict(img)
      classes_x=np.argmax(predict_x,axis=1)
      numbers = [0,1,2,3,4,5]
      classes = ['Buildings', 'Forest', 'Glaciers', 'Mountains', 'Sea', 'Street']
      dir_clases = dict(zip(numbers,classes))
    with col2:
      st.write(f'Model is **{predict_x[0][classes_x[0]]*100:.2f}%** sure that it is **{dir_clases[classes_x[0]]}**')
      dir_clases = dict(zip(predict_x[0],classes))
      import collections
      od = collections.OrderedDict(sorted(dir_clases.items(),reverse=True))
      
      # print to 5 accurate results.
      st.write('Other **top 5 possibilities** :')
      temp_increment = 1
      for key,values in od.items():
        if temp_increment != 1:
          st.write(f'{key*100:.2f}% - {values}')
        temp_increment += 1
        if temp_increment >=7:
          break
