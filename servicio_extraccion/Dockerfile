FROM python:3.8-alpine

RUN mkdir /usr/src/app/
COPY ./LecturaTextoImagen /usr/src/app/
WORKDIR /usr/src/app/

RUN apk update && apk add --no-cache python3-dev gcc libc-dev musl-dev linux-headers tesseract-ocr tesseract-ocr-data-spa
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5050

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]