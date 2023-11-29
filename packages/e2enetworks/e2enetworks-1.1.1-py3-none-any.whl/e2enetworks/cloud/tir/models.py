import json

import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL, BUCKET_TYPES, MODEL_TYPES, headers, MANAGED_STORAGE
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.cloud.tir.minio_service import MinioService
from e2enetworks.cloud.tir.helpers import get_random_string


class Models:
    def __init__(
            self,
            team: Optional[str] = "",
            project: Optional[str] = ""
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

    def create(self, name, model_type, storage_type=MANAGED_STORAGE, bucket_name=None):
        payload = json.dumps({
            "name": name,
            "model_type": model_type,
            "bucket_name": bucket_name,
            "storage_type": storage_type
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        response = prepare_object(response)
        return response

    def push_model(self, model_path, prefix="", model_id=None, model_type="custom"):
        if model_id:
            model = self.get(model_id)
            if model:
                access_key = model.access_key.access_key
                secret_key = model.access_key.secret_key
            else:
                raise ValueError("invalid model_id parameter")
        else:
            model_name = f"model{get_random_string(6)}"
            model = self.create(name=model_name, model_type=model_type, storage_type=MANAGED_STORAGE, bucket_name=None)
            if model:
                access_key = model.access_key.access_key
                secret_key = model.access_key.secret_key
            else:
                raise ValueError("failed to create a new model")

        minio_service = MinioService(access_key=access_key, secret_key=secret_key)
        minio_service.upload_directory_recursive(bucket_name=model.bucket.bucket_name,
                                                 source_directory=model_path, prefix=prefix)
        print("Model Pushed Successfully")
        if not model_id:
            return prepare_object(model)

    def download_model(self, model_id, local_path, prefix=""):
        if not model_id:
            raise ValueError("model id is mandatory")
        model = self.get(model_id)
        try:
            if model:
                access_key = model.access_key.access_key
                secret_key = model.access_key.secret_key
            else:
                raise ValueError("Invalid model id")
            minio_service = MinioService(access_key=access_key, secret_key=secret_key)
            minio_service.download_model(bucket_name=model.bucket.bucket_name, local_path=local_path, prefix=prefix)
            print("Model downloaded successfully")
        except Exception as e:
            print(e)
            raise ValueError("invalid model id")

    def get(self, model_id):

        if type(model_id) != int:
            raise ValueError(model_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/" \
              f"{model_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        response = prepare_object(response)
        return response

    def list(self):
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        response = prepare_object(response)
        return response

    def delete(self, model_id):
        if type(model_id) != int:
            raise ValueError(model_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/model/" \
              f"{model_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("Models Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to interact with models.")
        print("\t\tAvailable methods:")
        print(
            "\t\t1. __init__(team, project): Initializes a Models instance with the specified team and project "
            "IDs.")
        print("\t\t2. create(name, model_type, storage_type, bucket_name): Creates a new model with the provided "
              "details.")
        print("\t\t3. push_model(model_path, prefix, model_id, model_type): Creates a new model with the provided "
              "details.")
        print("\t\t4. download_model(model_id, local_path, prefix)")
        print("\t\t get(model_id): Retrieves information about a specific model using its ID.")
        print("\t\t list(): Lists all models associated with the team and project.")
        print("\t\t6. delete(model_id): Deletes a model with the given ID.")
        print("\t\t7. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tmodels = Models(123, 456)")
        print(f"\t\tmodels.create(name='Test Dataset', model_type={MODEL_TYPES}, , storage_type={BUCKET_TYPES}, "
              f"bucket_name='dataset-bucket'")
        print(f"\t\tmodels.push_model(model_path, prefix='', model_id=None, model_type='custom')")
        print(f"\t\tmodels.download_model(model_id=<model id>, local_path=<path of local directory>,"
              f" prefix=<prefix in teh bucket>)")
        print("\t\tmodels.get(789)")
        print("\t\tmodels.list()")
        print("\t\tmodels.delete(789)")