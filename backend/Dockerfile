FROM python:3.12.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir code
WORKDIR code
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /code/
#ADD .env /code/.env


CMD ["gunicorn", "--bind", "8000:8000", "foodgram.wsgi:application"]
