FROM python:3.11-rc-bullseye

ENV PYTHONFAULTHANDLER=1

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app

COPY requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python", "app.py", "--host", "0.0.0.0"]

