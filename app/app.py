import os
import src
from src.utils.config_loader import constants,Config
from src.utils import config_loader
from src.utils.script_utils import validate_config
import importlib
from flask import Flask,request,Response
import PIL
import PIL.Image
import cv2
import numpy as np
import base64
import io
from flask import render_template

model_config_path = os.path.join(constants.ARTIFACT_MODEL_DIR,"config.yaml")
config = Config(model_config_path)
# validate config
validate_config(config)

config_loader.config = config


# now load model
model_dir = constants.ARTIFACT_MODEL_DIR
model_save_path = os.path.join(model_dir,"model.weights.h5")

if not os.path.exists(model_save_path):
    raise Exception("No model found")

Model = importlib.import_module(f"src.{config.task}.model.models.{config.model}").Model
model = Model(model_save_path)


app = Flask(__name__)


@app.route("/",methods=["GET"])
def home():
    # return "home page"
    return render_template("index.html")

@app.route("/config",methods=["GET"])
def read_config():
    content = open(model_config_path,"r").read()
    return Response(content,mimetype='text')

@app.route("/colorize",methods=["POST"])
def colorize():
    
    files = request.files
    file = files.get('image')
    print(file)
    img = PIL.Image.open(file)
    img = img.convert("L")
    
    img = img.resize([config.image_size,config.image_size])
    img = np.array(img)
    print(img.min(),img.max())
    print(img.shape)

    # model.predict()
    L = img[:,:,None]
    L = (L/255*100).astype("uint8")
    
    AB = model.predict(L[None])[0]
    img = np.concatenate([L, AB], axis=-1)
    colored_img = cv2.cvtColor(img, cv2.COLOR_LAB2RGB) * 255

    print(colored_img.shape)

    im = PIL.Image.fromarray(colored_img.astype("uint8"))
    rawBytes = io.BytesIO()
    im.save(rawBytes, "jpeg")
    rawBytes.seek(0)
    base64_img = (base64.b64encode(rawBytes.read())).decode("utf-8")
    
    return {"image":base64_img}


app.run(debug=True,host="0.0.0.0",port=5000)