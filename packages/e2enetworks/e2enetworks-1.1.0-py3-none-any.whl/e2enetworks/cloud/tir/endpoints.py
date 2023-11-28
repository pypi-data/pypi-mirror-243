import json

import requests

from typing import Optional
from e2enetworks.constants import BASE_GPU_URL, headers, TRITON, PYTORCH
from e2enetworks.cloud.tir import client, Plans
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.cloud.tir.helpers import plan_to_sku_id
from e2enetworks.cloud.tir.skus import Plans

containers = {
    "llma": "amole2e/meta-7b",
    "llma_eos": "amole2e/meta-7b-chat",
    "codellama": "aimle2e/codellama",
    "codellama_eos": "aimle2e/codellama-eos",
    "mpt": "aimle2e/mpt-7b-chat:hf-v3",
    "mpt_eos": "aimle2e/mpt-7b-chat:eos-v2",
    "stable_diffusion": "aimle2e/stable-diffusion-2-1:hf-v1",
    "stable_diffusion_eos": "aimle2e/stable-diffusion-2-1:eos-v1"
}


class EndPoints:
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

    def list_plans(self):
        return Plans().list_endpoint_plans()

    def get_container_name(self, container_name, model_id, framework):
        if framework == "custom":
            return container_name
        if model_id:
            return containers[framework+'_eos'] if framework+'_eos' in containers else None
        else:
            return containers[framework] if framework in containers else None

    def create_triton(self, endpoint_name, plan, model_id, model_path='', replicas=1):
        if not endpoint_name:
            raise ValueError(endpoint_name)
        if not plan:
            raise ValueError(plan)
        if not model_id:
            raise ValueError(model_id)

        return self.create_inference_for_framework(endpoint_name=endpoint_name,
                                                   plan=plan,
                                                   model_path=model_path,
                                                   model_id=model_id,
                                                   replicas=replicas,
                                                   framework=TRITON)

    def create_pytorch(self, endpoint_name, plan, model_id, model_path='', replicas=1):
        if not endpoint_name:
            raise ValueError(endpoint_name)
        if not plan:
            raise ValueError(plan)
        if not model_id:
            raise ValueError(model_id)

        return self.create_inference_for_framework(endpoint_name=endpoint_name,
                                                   plan=plan,
                                                   model_path=model_path,
                                                   model_id=model_id,
                                                   replicas=replicas,
                                                   framework=PYTORCH)

    def create_inference_for_framework(self, endpoint_name, plan, model_path, model_id, replicas, framework):
        skus = Plans().get_skus_list("inference_service")
        sku_id = plan_to_sku_id(skus=skus, plan=plan)

        if not sku_id:
            raise ValueError(plan)

        payload = json.dumps({
            "name": endpoint_name or "",
            "path": model_path,
            "custom_endpoint_details": {},
            "model_id": model_id,
            "sku_id": sku_id,
            "replica": replicas,
            "framework": framework,
            "auto_scale_policy": {
                "min_replicas": replicas,
                "max_replicas": replicas,
                "rules": [
                    {
                        "metric": "cpu",
                        "condition_type": "limit",
                        "value": "80",
                        "watch_period": "15"
                    }
                ],
                "stability_period": "60"
            }
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        print(f"To check the Inference Status and logs, PLease visit "
              f"https://gpu-notebooks.e2enetworks.com/projects/{client.Default.project()}/model-endpoints")
        return prepare_object(response)

    def create(self, endpoint_name, framework, plan, model_id=None, container_name=None, container_type="public",
               replicas=1, disc_size=0, model_path="", env_variables=[], mount_path="", registry_endpoint="",
               auth_type="pass", username="", password="", docker_config=""):
        if not endpoint_name:
            raise ValueError(endpoint_name)
        if not framework:
            raise ValueError(framework)
        if not plan:
            raise ValueError(plan)

        skus = Plans().get_skus_list("inference_service")
        sku_id = plan_to_sku_id(skus=skus, plan=plan)

        if not sku_id:
            raise ValueError(plan)

        container_name = self.get_container_name(container_name=container_name, model_id=model_id, framework=framework)

        if framework not in ["pytorch", "triton"] and not container_name:
            raise ValueError(container_name)

        payload = json.dumps({
            "name": endpoint_name or "",
            "path": model_path,
            "custom_endpoint_details": {
                "container": {
                    "container_name": container_name,
                    "container_type": container_type,
                    "private_image_details": {
                        "registry_endpoint": registry_endpoint,
                        "auth_type": auth_type,
                        "password_auth_details": {
                            "username": username,
                            "password": password
                        },
                        "docker_config": {
                            "code": docker_config
                        }
                    }
                },
                "resource_details": {
                    "disk_size": disc_size,
                    "mount_path": mount_path,
                    "env_variables": env_variables
                },
            },
            "model_id": model_id,
            "sku_id": sku_id,
            "replica": replicas or 1,
            "framework": framework
        })
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/?" \
              f"apikey={client.Default.api_key()}"
        response = requests.post(url=url, headers=headers, data=payload)
        print(f"To check the Inference Status and logs, PLease visit "
              f"https://gpu-notebooks.e2enetworks.com/projects/{client.Default.project()}/model-endpoints")
        return prepare_object(response)

    def get(self, endpoint_id):

        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def logs(self, endpoint_id):

        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/logs/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def start(self, endpoint_id):
        payload = json.dumps({
            "action": "start"
        })
        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/"
        req = requests.Request('PUT', url=url, data=payload, headers=headers)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def stop(self, endpoint_id):
        payload = json.dumps({
            "action": "stop"
        })
        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)
        headers['Authorization'] = f'Bearer {client.Default.access_token()}'
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/"
        req = requests.Request('PUT', url=url, data=payload, headers=headers)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list(self):
        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete(self, endpoint_id):
        if type(endpoint_id) != int:
            raise ValueError(endpoint_id)

        url = f"{BASE_GPU_URL}teams/{client.Default.team()}/projects/{client.Default.project()}/serving/inference/" \
              f"{endpoint_id}/"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        print("EndPoint Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to interact with EndPoint.")
        print("\t\tAvailable methods:")
        print("\t\t1. __init__(team, project): Initializes an EndPoints instance with the specified team and "
              "project IDs.")
        print("\t\t2. list_plans()")
        print("\t\t3. create_triton(endpoint_name, plan, model_id, model_path='', replicas=1)")
        print("\t\t4. create_pytorch(endpoint_name, plan, model_id, model_path='', replicas=1)")
        print("\t\t5. create(endpoint_name, framework, plan, container_name, container_type, model_id, replicas=1, "
              "disc_size=10, model_path="", env_variables=[], mount_path="", registry_endpoint="", "
              "auth_type='pass', username="", password="", docker_config=""): "
              "Creates an endpoint with the provided details.")
        print("\t\t6. get(endpoint_id): Retrieves information about a specific endpoint using its ID.")
        print("\t\t7. logs(endpoint_id): Retrieves logs of a specific endpoint using its ID.")
        print("\t\t8. stop(endpoint_id): Stops a specific endpoint using its ID.")
        print("\t\t9. start(endpoint_id): Starts a specific endpoint using its ID.")
        print("\t\t10. list(): Lists all endpoints associated with the team and project.")
        print("\t\t11. delete(endpoint_id): Deletes an endpoint with the given ID.")
        print("\t\t12. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tendpoints = EndPoints(123, 456)")
        print("\t\tendpoints.create("
              "\n\t\t\t\tendpoint_name(required):String => 'Name of Endpoint'",
              "\n\t\t\t\tframework(required):String => '['triton', 'pytorch', 'llma', 'stable_diffusion', 'mpt,"
              "\n\t\t\t\t\t'codellama', 'custom']'",
              "\n\t\t\t\tplan(required):String=> Plans Can be listed using tir.Plans Apis",
              "\n\t\t\t\tcontainer_type(optional):String=> Default value is public and "
              "\n\t\t\t\t\tallowed values are [public, private]",
              "\n\t\t\t\tmodel_id:Integer=> Required in case of Framework type=[triton, pytorch] and "
              "\n\t\t\t\t\tif model is stored in EOS",
              "\n\t\t\t\tcontainer_name(optional):String=> Docker Container Image Name required in case of Custom "
              "\n\t\t\t\tContainer Only",
              "\n\t\t\t\treplicas(optional):Integer=> Default value id 1",
              "\n\t\t\t\tdisc_size(optional):Integer=> Default value id 10Gb",
              "\n\t\t\t\tmodel_path(optional):String=> Path of EOS bucket where the model is stored",
              "\n\t\t\t\tenv_variables(optional):List=> Env variables can be passed as "
              "\n\t\t\t\t\t[{ 'key': '', 'value': '/mnt/models'}]"
              "\n\t\t\t\tmount_path(optional):String=> Default value is '/mnt/models'"
              "\n\t\t\t\tregistry_endpoint(optional):String=> Required in Case of container_type=private"
              "\n\t\t\t\tauth_type(optional):String=> Required in case of container_type=private, "
              "\n\t\t\t\t\tAllowed Values are ['pass', 'docker'] "
              "\n\t\t\t\t\tDefault Value is pass'"
              "\n\t\t\t\tusername(optional):String=> Required in case of container_type=private and auth_type=pass"
              "\n\t\t\t\tusername(optional):String=> Required in case of container_type=private and auth_type=pass"
              "\n\t\t\t\tdocker_config(optional):String=> Required in case of container_type=private and "
              "auth_type=docker")
        print("\t\tendpoints.get(789)")
        print("\t\tendpoints.logs(789)")
        print("\t\tendpoints.stop(789)")
        print("\t\tendpoints.start(789)")
        print("\t\tendpoints.list()")
        print("\t\tendpoints.delete(789)")
