FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY ./requirementsdock.txt /requirementsdock.txt

RUN pip --no-cache-dir install --upgrade pip
# RUN apk add --update --no-cache postgresql-client jpeg-dev
# RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --no-cache-dir -r requirementsdock.txt
# RUN apk del .tmp-build-deps
RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app
# Environment Variables


EXPOSE 5001

