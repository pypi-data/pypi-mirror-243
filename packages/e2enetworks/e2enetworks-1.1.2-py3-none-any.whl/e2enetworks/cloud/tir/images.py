import requests
from prettytable import PrettyTable

from e2enetworks.cloud.tir import client
from e2enetworks.constants import BASE_GPU_URL


class Images:
    def __init__(self):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

    def list(self):
        url = f"{BASE_GPU_URL}gpu_service/image/"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        if response.status_code == 200:
            images = response.json()["data"]
            images_table = PrettyTable()
            images_table.field_names = ['Name', 'version', 'image_id']
            for image in images:
                images_table.add_row([image.get('name'), image.get('version'), image.get('id')])
            return images_table


    @staticmethod
    def help():
        print("Images Class Help")
        print("\t\t================")
        print("\t\tThis class provides functionalities to interact with Images.")
        print("\t\tAvailable methods:")

        print("\t\t1. list(): Lists all Images.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\timages = Images()")
        print("\t\timages.list()")
