import boto3
from decouple import config

BUCKET_NAME = config("BUCKET_NAME")

s3 = boto3.client("s3")

# List all buckets
buckets_resp = s3.list_buckets()
for bucket in buckets_resp["Buckets"]:
    print("bucket:", bucket)

# List all objects in a bucket
response = s3.list_objects_v2(Bucket=BUCKET_NAME)
key_count = response["KeyCount"]
print(f"Key count: {key_count}")