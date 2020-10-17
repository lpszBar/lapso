FROM python:3.7.4-alpine3.10

ARG LAPSO_S3_BUCKET_NAME
ARG LAPSO_S3_ACCESS_KEY
ARG LAPSO_S3_SECRET_ACCESS_KEY

ENV S3_BUCKET_NAME $LAPSO_S3_BUCKET_NAME
ENV S3_ACCESS_KEY $LAPSO_S3_ACCESS_KEY
ENV S3_SECRET_ACCESS_KEY $LAPSO_S3_SECRET_ACCESS_KEY

RUN apk add --no-cache sqlite zlib-dev jpeg-dev build-base python-dev npm

RUN pip install flask==1.1.1 boto3==1.9.196 Pillow==6.1.0 Flask-Login==0.4.1 Flask-CORS==3.0.8
#tests
RUN pip install pytest==5.1.1 pycodestyle==2.5.0

#ENV LIBRARY_PATH=/lib:/usr/lib  # not sure if this is used for pillow

COPY . /app

WORKDIR /app
ENTRYPOINT  ["sh"]
CMD ["init-app.sh"]
