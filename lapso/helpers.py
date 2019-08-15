import boto3
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION
import string
import random

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'gif', 'png']

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(filepath, filename, content_type,
                      bucket_name, acl="public-read"):
    assert bucket_name
    assert filename
    assert filepath

    try:
        s3.upload_file(
            filepath,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        raise e

    return "{}{}".format(S3_LOCATION, filename)


def random_string(length):
    return ''.join(random.choice(string.ascii_letters+string.digits)
                   for i in range(length))
