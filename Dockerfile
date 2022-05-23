FROM python:3.10-bullseye

RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

RUN mkdir -p /home/flask/app
WORKDIR /home/flask/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /home/flask/app

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /home/flask/app

RUN chown -R flask:flaskgroup /home/flask
USER flask

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000:5100
CMD ["python", "app.py", "--host", "0.0.0.0"]