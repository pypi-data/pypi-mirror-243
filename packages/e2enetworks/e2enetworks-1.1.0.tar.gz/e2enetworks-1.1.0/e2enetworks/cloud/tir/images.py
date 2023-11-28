import requests

from e2enetworks.cloud.tir import client
from e2enetworks.constants import BASE_GPU_URL

id_to_hash_code_mapping = {
    1: "QHeMSAyC",
    2: "skqbtZpd",
    3: "NynWPeEJ",
    4: "XEFKbStA",
    5: "QPSKEFKQ",
    6: "siGeSJyO",
    7: "yYkVtTsC",
    8: "wVOqCnpB",
    9: "SICGgpoZ",
    10: "ddUybAyh",
    11: "yWNKwMlg",
    12: "WtZaGkNZ"
}


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
            print("Code               | Name")
            for image in images:
                print(f"{id_to_hash_code_mapping.get(image.get('id'))}           |{image.get('name')} {image.get('version')}")


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
