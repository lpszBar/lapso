FROM python:3.7.4-alpine3.10

ARG LAPSO_S3_BUCKET_NAME
ARG LAPSO_S3_ACCESS_KEY
ARG LAPSO_S3_SECRET_ACCESS_KEY

ENV S3_BUCKET_NAME $LAPSO_S3_BUCKET_NAME
ENV S3_ACCESS_KEY $LAPSO_S3_ACCESS_KEY
ENV S3_SECRET_ACCESS_KEY $LAPSO_S3_SECRET_ACCESS_KEY

RUN apk add --no-cache sqlite zlib-dev jpeg-dev build-base python-dev

RUN pip install flask==1.1.1 boto3==1.9.196 Pillow==6.1.0 Flask-Login==0.4.1
#tests
RUN pip install mamba==0.10 expects==0.9.0 pycodestyle==2.5.0

#ENV LIBRARY_PATH=/lib:/usr/lib  # not sure if this is used for pillow

WORKDIR /app
ENTRYPOINT  ["sh"]
CMD ["init-app.sh"]
