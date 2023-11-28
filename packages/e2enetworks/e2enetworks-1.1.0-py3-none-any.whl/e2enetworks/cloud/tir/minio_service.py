from minio import Minio
from minio.error import S3Error
import os

from e2enetworks.constants import S3_ENDPOINT


class MinioService:

    def __init__(self, access_key, secret_key, endpoint=S3_ENDPOINT):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = Minio(endpoint, access_key, secret_key)

    def upload_directory_recursive(self, bucket_name, source_directory, prefix=""):
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                file_path = os.path.join(root, file)
                object_name = os.path.join(prefix, os.path.relpath(file_path, source_directory))
                try:
                    self.client.fput_object(bucket_name, object_name, file_path)
                    print(f"Uploaded {object_name}")
                except S3Error as e:
                    print(f"Error uploading {object_name}: {e}")

    def download_model(self, bucket_name, local_path, prefix=""):
        objects = self.client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True)
        for obj in objects:
            object_name = obj.object_name
            try:
                self.client.fget_object(bucket_name, object_name, f"{local_path}/{object_name}")
                print(f"Downloaded: {object_name}")
            except Exception as err:
                print(f"Error downloading {object_name}: {err}")
