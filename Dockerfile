FROM python:3.10

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y ffmpeg libcogl-pango-dev

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]