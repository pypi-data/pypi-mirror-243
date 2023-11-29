import json
from typing import Optional

import requests

from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.minio_service import MinioService
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.constants import BASE_GPU_URL, BUCKET_TYPES, headers


class Datasets:
    def __init__(
            self,
            team: Optional[str] = "",
            project: Optional[str] = "",
    ):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

        if project:
            client.Default.set_project(project)

        if team:
            client.Default.set_team(team)

    def create(self, name=None, bucket_name=None, bucket_type=None, description=""):
        payload = json.dumps({
            "type": bucket_type,
            "name": name,
            "bucket_name": bucket_name,
            "description": description,
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        return prepare_object(response)

    def get(self, dataset_id):

        if type(dataset_id) != int:
            raise ValueError(dataset_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/" \
              f"{dataset_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, dataset_id):
        if type(dataset_id) != int:
            raise ValueError(dataset_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/datasets/" \
              f"{dataset_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)
    
    def upload_dataset(self, dataset_path, prefix="", dataset_id=None):
        dataset = self.get(dataset_id) if dataset_id else None
        if dataset:
            access_key = dataset.access_key.access_key
            secret_key = dataset.access_key.secret_key
        else:
            raise ValueError("invalid dataset_id parameter")
        minio_service = MinioService(access_key=access_key, secret_key=secret_key)
        minio_service.upload_directory_recursive(bucket_name=dataset.bucket.bucket_name,
                                                 source_directory=dataset_path, prefix=prefix)
        print("Dataset Pushed Successfully")
        if not dataset_id:
            return prepare_object(dataset)

    def download_dataset(self, dataset_id, local_path, prefix=""):
        dataset = self.get(dataset_id) if dataset_id else None
        try:
            if dataset:
                access_key = dataset.access_key.access_key
                secret_key = dataset.access_key.secret_key
            else:
                raise ValueError("Invalid dataset id")
            minio_service = MinioService(access_key=access_key, secret_key=secret_key)
            minio_service.download_directory_recursive(bucket_name=dataset.bucket.bucket_name, 
                                                       local_path=local_path, prefix=prefix)
            print("dataset downloaded successfully")
        except Exception as e:
            print(e)
            raise ValueError("invalid dataset id")

    @staticmethod
    def help():
        print("Datasets Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to interact with Datasets.")
        print("\t\tAvailable methods:")
        print(
            "\t\t1. __init__(team, project): Initializes a Datasets instance with the specified team and "
            "project IDs.")
        print(f"\t\t2. create(name, bucket_name=, bucket_type, description): Creates a new dataset with the provided"
              f"name, bucket name, bucket type and description\n Bucket Name is not required in case of"
              f" bucket_type='managed'")
        print("\t\t3. get(bucket_name): Retrieves information about a specific dataset using its bucket name.")
        print("\t\t4. list(): Lists all datasets associated with the team and project.")
        print("\t\t5. delete(dataset_id): Deletes a dataset with the given dataset_id")
        print("\t\t3. push_dataset(dataset_path, prefix, dataset_id): Creates a new dataset with the provided "
              "details.")
        print("\t\t4. download_dataset(dataset_id, local_path, prefix)")
        print("\t\t8. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tdatasets = Datasets(123, 456)")
        print(f"\t\tdatasets.create(name='Test Dataset', bucket_name='dataset-bucket', bucket_type={BUCKET_TYPES},"
              f" description='Test Dataset')")
        print("\t\tdatasets.get('Bucket Name')")
        print("\t\tdatasets.list()")
        print("\t\tdatasets.delete(236)")
        print(f"\t\tdatasets.push_dataset(dataset_path, prefix='', dataset_id=None)")
        print(f"\t\tdatasets.download_dataset(dataset_id=<dataset id>, local_path=<path of local directory>,"
              f" prefix=<prefix in the bucket>)")