from loguru import logger
from tempfile import NamedTemporaryFile

from azure.storage.blob import BlobServiceClient
from google.cloud import storage
from google.oauth2 import service_account
import boto3


class ObjectStorageClient:
    def __init__(self, bucket_config: dict, default_minio_client):
        self.client_type = None
        self.client = None
        if "virtual_bucket_path" in bucket_config["settings"]:
            self.client_type = "MINIO"
            self.client = default_minio_client
            self.virtual_bucket_path = bucket_config["settings"]["virtual_bucket_path"]
        else:
            self.client_type = bucket_config["settings"]["kind"]
            if self.client_type == "AZURE_OBJECT_STORAGE_SETTINGS":
                account_name = bucket_config["settings"]["account_name"]
                account_key = bucket_config["settings"]["account_key"]

                connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
                self.client = BlobServiceClient.from_connection_string(connect_str)
            elif self.client_type == "GC_OBJECT_STORAGE_SETTINGS":
                private_key_id = bucket_config["settings"]["private_key_id"]
                private_key = bucket_config["settings"]["private_key"]
                client_email = bucket_config["settings"]["email"]

                credentials_dict = {
                    "type": "service_account",
                    "private_key_id": private_key_id,
                    "private_key": private_key,
                    "client_email": client_email,
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
                credentials = service_account.Credentials.from_service_account_info(credentials_dict)
                self.client = storage.Client(credentials=credentials)
            elif self.client_type == "S3_OBJECT_STORAGE_SETTINGS":
                endpoint = bucket_config["settings"]["endpoint"]
                access_key = bucket_config["settings"]["access_key"]
                secret_key = bucket_config["settings"]["secret_key"]

                self.client = boto3.client(
                    's3',
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    endpoint_url=endpoint
                )
            else:
                logger.error(f"Object storage {bucket_config['settings']['kind']} not supported.")

    def list_bucket_objects(self, bucket_name: str, prefix: str = "", recursive: bool = True):
        if self.client_type == "MINIO":
            return [obj.object_name.replace(self.virtual_bucket_path + '/', "", 1) for obj in self.client.list_objects(
                bucket_name,
                self.virtual_bucket_path + '/' + prefix,
                recursive
            )]
        elif self.client_type == "AZURE_OBJECT_STORAGE_SETTINGS":
            bucket = self.client.get_container_client(bucket_name)
            list_objects = list(bucket.list_blob_names(name_starts_with=prefix))
            return list_objects if recursive else [obj for obj in list_objects if
                                                   '/' not in obj[len(prefix):].lstrip('/')]
        elif self.client_type == "S3_OBJECT_STORAGE_SETTINGS":
            list_objects = [obj["Key"] for obj in
                            self.client.list_objects(Bucket=bucket_name, Prefix=prefix)["Contents"] if
                            not obj["Key"].endswith("/")]
            return list_objects if recursive else [obj for obj in list_objects if
                                                   '/' not in obj[len(prefix):].lstrip('/')]
        elif self.client_type == "GC_OBJECT_STORAGE_SETTINGS":
            bucket = self.client.get_bucket(bucket_name)
            list_objects = [obj.name for obj in bucket.list_blobs(prefix=prefix) if not obj.name.endswith("/")]
            return list_objects if recursive else [obj for obj in list_objects if
                                                   '/' not in obj[len(prefix):].lstrip('/')]

    def read_from_bucket_to_file(self, bucket_name: str, object_name: str):
        with NamedTemporaryFile(delete=False) as f:
            if self.client_type == "MINIO":
                self.client.fget_object(bucket_name, self.virtual_bucket_path + '/' + object_name, f.name)
            elif self.client_type == "AZURE_OBJECT_STORAGE_SETTINGS":
                bucket = self.client.get_container_client(bucket_name)
                f.write(bucket.download_blob(object_name).readall())
            elif self.client_type == "S3_OBJECT_STORAGE_SETTINGS":
                self.client.download_fileobj(bucket_name, object_name, f)
            elif self.client_type == "GC_OBJECT_STORAGE_SETTINGS":
                bucket = self.client.get_bucket(bucket_name)
                blob = storage.Blob(object_name, bucket)
                self.client.download_blob_to_file(blob, f)
            f.close()
            return f.name

    def write_file_in_bucket(self, bucket_name: str, file_name: str, data):
        data.seek(0)
        if self.client_type == "MINIO":
            self.client.put_object(
                bucket_name,
                self.virtual_bucket_path + '/' + file_name,
                data,
                length=data.getbuffer().nbytes
            )
        elif self.client_type == "AZURE_OBJECT_STORAGE_SETTINGS":
            blob_client = self.client.get_blob_client(container=bucket_name, blob=file_name)
            blob_client.upload_blob(data)
        elif self.client_type == "S3_OBJECT_STORAGE_SETTINGS":
            self.client.upload_fileobj(data, bucket_name, file_name)
        elif self.client_type == "GC_OBJECT_STORAGE_SETTINGS":
            bucket = self.client.get_bucket(bucket_name)
            blob = bucket.blob(file_name)
            blob.upload_from_file(data)
