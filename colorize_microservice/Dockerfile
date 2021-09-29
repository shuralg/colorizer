FROM python:3.7

RUN python -m pip install torch==1.9.1+cpu torchvision==0.10.1+cpu torchaudio==0.9.1 \
    -f https://download.pytorch.org/whl/torch_stable.html \
    && python -m pip install flask==2.0.1 flask-cors==3.0.10 gunicorn numpy==1.21.2 pillow==8.3.2

WORKDIR /app

ADD settings.py settings.py
ADD models.py models.py
ADD generator_19.pth generator_19.pth
ADD colorizer.py colorizer.py

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "colorizer:app" ]

