FROM python:3.10-alpine

WORKDIR /app

RUN apk update
RUN apk add alpine-sdk ffmpeg pango-dev font-linux-libertine

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]