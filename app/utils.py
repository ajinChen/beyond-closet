import yaml
import time
import sys
from werkzeug.utils import secure_filename
from flask import request


# Load yaml file
def get_yaml_file(filepath = "./static/team_members.yaml"):
    # about page yaml file
    with open(filepath, 'r') as stream:
        try:
            team_members_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return team_members_yaml


# S3 bucket connector
def upload_clothing_jpeg_to_s3(s3, bucket_name, user_id, image_file, style):
    ts = int(time.time())
    filename = secure_filename(f"{user_id}_{ts}_{style}.jpeg")
    try:
        s3.put_object(Body=image_file,
            Bucket=bucket_name,
            Key=filename,
            ContentType=request.mimetype)
    except Exception as e:
        print(f"Something Happened: {e}", file=sys.stderr)
        return f'''<!DOCTYPE html><html><body><p>{str(e)}</p></body></html>'''
    # after upload file to s3 bucket, return filename of the uploaded file
    region = 'us-west-2'
    url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{filename}"
    return url