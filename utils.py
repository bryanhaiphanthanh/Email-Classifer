import boto3
from botocore.config import Config

def get_session():
    return boto3.Session(aws_access_key_id="XXXXXXXXXXXXXXXXXXXX", aws_secret_access_key= "XXXXXXXXXXXXXXXXXXXX")

def get_polly_client():
    session = get_session()
    return session.client('polly', 'ca-central-1')

def get_rekonition_client():
    session = get_session()
    return session.client('rekognition',  'us-east-2')

def get_s3_client():
    session = get_session()
    return session.client('s3', 'us-east-2')