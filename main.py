# -*- coding: utf-8 -*-

from flask import Flask , render_template, request, redirect, flash
import cv2
from sklearn.cluster import KMeans
from time import sleep
import numpy as np
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './/img/'

def get_color(img, n):
  img = img.reshape((img.shape[0] * img.shape[1] ), 3)
  kmeans = KMeans(n_clusters=n)
  kmeans.fit(img)
  colors = kmeans.cluster_centers_
  return colors.astype(int)



def give_color(file):

  print('file : ',file)
  img = cv2.imread(file)

  filename = 'colors_'+file
  print('filename : ',filename)
  cluster = 5

  colors = get_color(img, cluster)
  print(colors)
  next = np.zeros((500,500,3), dtype = np.uint8)
  next[:, :100] = colors[0]
  next[:, 100:200] = colors[1]
  next[:, 200:300] = colors[2]
  next[:, 300:400] = colors[3]
  next[:, 400:] = colors[4]
  #cv2.imshow('kamera', img)
  #cv2.imshow('Colorbar', next)
  cv2.imwrite(filename, next)
  cv2.imwrite('static/color.png', next)
  cv2.imwrite('static/img.png', img)
  #cv2.waitKey()
  #cv2.destroyAllWindows()



@app.route('/', methods = ['POST', 'GET'] )
def main():
  if request.method == 'POST':
    image = request.files['img']
    filename = image.filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    sleep(1)
    give_color('img/'+filename)

    return render_template('index.html')

  else:
    return render_template('index.html')

app.run(debug=True, port=5454)