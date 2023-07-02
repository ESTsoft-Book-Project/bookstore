from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage

class MediaStorage(S3Boto3Storage):
    location = "media"

class StaticFileStorage(S3StaticStorage):
    location = "static"
