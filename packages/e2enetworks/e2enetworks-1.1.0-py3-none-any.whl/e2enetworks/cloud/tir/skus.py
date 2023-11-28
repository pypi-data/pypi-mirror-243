import requests
from e2enetworks.constants import BASE_GPU_URL, hash_code_to_image_id
from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.helpers import cpu_plan_short_code, gpu_plan_short_code
from e2enetworks.cloud.tir.utils import prepare_object


class Plans:
    def __init__(self):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

    def list_endpoint_plans(self):
        return self.list("inference_service")

    def list(self, service, image=None):

        if type(service) != str:
            print(f"Service - {service} Should be String")
            return

        if service == "notebook" and type(image) != str:
            print(f"Image ID - {image} Should be String")
            return
        image = hash_code_to_image_id.get(image)
        image = image if image else ""
        url = f"{BASE_GPU_URL}gpu_service/sku/?image_id={image}&service={service}&"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        if response.status_code == 200:
            skus = response.json()["data"]
            for sku in skus["CPU"]:
                if sku.get("is_inventory_available"):
                    print(cpu_plan_short_code(sku))
            for sku in skus["GPU"]:
                if sku.get("is_inventory_available"):
                    print(gpu_plan_short_code(sku))

    def get_skus_list(self, service, image=None):
        image = image if image else ""
        url = f"{BASE_GPU_URL}gpu_service/sku/?image_id={image}&service={service}&"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return response.json()["data"] if response.status_code == 200 else prepare_object(response)

    @staticmethod
    def help():
        print("Sku Class Help")
        print("\t\t================")
        print("\t\tThis class provides functionalities to interact with Plans.")
        print("\t\tAvailable methods:")
        print("\t\t- list_endpoint_plans: List Available Endpoint Plans")
        print("\t\t1. list(service, image_id): Lists all Plans for given image_id and service.\n")
        print("\t\t Allowed Services List - ['notebook', 'inference_service', 'pipeline']")
        # Example usages
        print("\t\tExample usages:")
        print("\t\tskus = Plans()")
        print("\t\tskus.list('inference')")
