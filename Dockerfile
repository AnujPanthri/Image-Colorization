FROM tensorflow/tensorflow

EXPOSE 5000
COPY . /app
WORKDIR /app

# opencv fix
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install --ignore-installed -r requirements.txt --no-cache-dir
RUN pip install -e .

RUN ls -lh
RUN rm -r outputs
RUN ls -lh

RUN --mount=type=secret,id=COMET_API_KEY,mode=0444,required=true \
    python3 download_model_comet.py --key $(cat /run/secrets/COMET_API_KEY) --version 1.0.0

RUN chmod g+w /app
CMD python3 app/app.py