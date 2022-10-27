# importing libraries
import os
from keras.models import load_model
from keras_preprocessing.image import load_img,img_to_array
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# List of Classes to proide to prediction function
classes = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]


# Doggie Breeds
gcjcjvhvkv = """lab = [
 'Afghan', 'African Wild Dog', 'Airedale', 'American Hairless', 'American Spaniel', 
 'Basenji', 'Basset', 'Beagle', 'Bearded Collie', 'Bermaise',  'Bichon Frise',  'Blenheim',
     'Bloodhound',  'Bluetick',  'Border Collie',  'Borzoi',  'Boston Terrier',  'Boxer', 
     'Bull Mastiff',  'Bull Terrier',  'Bulldog',  'Cairn',  'Chihuahua',  'Chinese Crested', 
     'Chow',  'Clumber',  'Cockapoo',  'Cocker',  'Collie',  'Corgi', 'Coyote',  'Dalmation',
     'Dhole', 'Dingo', 'Doberman', 'Elk Hound', 'French Bulldog', 'German Sheperd', 
     'Golden Retriever', 'Great Dane', 'Great Perenees', 'Greyhound', 'Groenendael',
     'Irish Spaniel', 'Irish Wolfhound', 'Japanese Spaniel', 'Komondor', 'Labradoodle', 
     'Labrador', 'Lhasa', 'Malinois', 'Maltese', 'Mex Hairless', 'Newfoundland', 
     'Pekinese', 'Pit Bull', 'Pomeranian', 'Poodle', 'Pug', 'Rhodesian', 'Rottweiler', 
     'Saint Bernard', 'Schnauzer', 'Scotch Terrier', 'Shar_Pei', 'Shiba Inu', 'Shih-Tzu', 
     'Siberian Husky', 'Vizsla', 'Yorkie'
    ]"""

# Load Model
model1 = load_model('model.h5',compile=True)

# Prediction Function
def output(location):
    img=load_img(location,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255    
    img=np.expand_dims(img,[0])
    answer=model1.predict(img)
    y_class = answer.argmax(axis=-1)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = lab[y]
    return res

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['File']
        print('===================================================\n')
        print('Secure File          '+secure_filename(f.filename))
        fs = secure_filename(f.filename)
        f.save(fs)
        y = output(fs)

        if os.path.exists(fs):
            os.remove(fs)
            print('File Removed')
        else:
            print("The file does not exist")
        
        print('File Saved File Saved \n===================================================')
        data = "{data: "+y+" }"
        return jsonify(data)

    if request.method == 'GET':
        return "Hello World!!!"

# Driver Funtion
if __name__ == '__main__':
    app.run(debug=True, port=5002)