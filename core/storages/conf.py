from core.env import config

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_ADDRESSING_STYLE = "virtual"

AWS_STORAGE_BUCKET_NAME=config("AWS_STORAGE_BUCKET_NAME", default="estsoft-ormi-bookstore")
AWS_S3_REGION_NAME="ap-northeast-2"
AWS_S3_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

AWS_DEFAULT_ACL="public-read"
AWS_S3_USE_SSL=True


DEFAULT_FILE_STORAGE = 'core.storages.backends.MediaStorage'
STATICFILES_STORAGE = 'core.storages.backends.StaticFileStorage'