FROM python:3.7.6-alpine

RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps

RUN mkdir /Stardox
WORKDIR /Stardox
COPY . /Stardox

RUN pip install -r requirements.txt

RUN mkdir -p /root/Desktop

ENTRYPOINT [ "python", "/Stardox/src/stardox.py" ]
