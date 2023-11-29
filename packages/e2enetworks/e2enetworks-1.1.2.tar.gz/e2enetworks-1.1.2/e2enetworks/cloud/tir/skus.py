import requests
from prettytable import PrettyTable

from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.helpers import (cpu_plan_short_code,
                                           gpu_plan_short_code)
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.constants import BASE_GPU_URL, INFERENCE, NOTEBOOK


class Plans:
    def __init__(self):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

    def list_endpoint_plans(self):
        skus = self.list(INFERENCE)

        for sku in skus["CPU"]:
            if sku.get("is_inventory_available"):
                print(cpu_plan_short_code(sku))
        for sku in skus["GPU"]:
            if sku.get("is_inventory_available"):
                print(gpu_plan_short_code(sku))

    def list(self, service, image=None):

        if type(service) != str:
            print(f"Service - {service} Should be String")
            return

        if service == NOTEBOOK and type(image) != str:
            print(f"Image ID - {image} Should be String")
            return
        image = image if image else ""
        url = f"{BASE_GPU_URL}gpu_service/sku/?image_id={image}&service={service}&"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        skus = {}
        if response.status_code == 200:
            skus = response.json()["data"]
        return skus

    def get_skus_list(self, service, image=None):
        image = image if image else ""
        url = f"{BASE_GPU_URL}gpu_service/sku/?image_id={image}&service={service}&"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return response.json()["data"] if response.status_code == 200 else prepare_object(response)

    def get_notebook_plans_name(self, image=None):
            image = str(image) if image else ""
            plans = self.list(NOTEBOOK, image)
            for sku in plans["CPU"]:
                if sku.get("is_inventory_available"):
                    print(cpu_plan_short_code(sku))
            for sku in plans["GPU"]:
                if sku.get("is_inventory_available"):
                    print(gpu_plan_short_code(sku))

    def get_notebook_plans_list(self, image=None):
        image = str(image) if image else ""
        plans = self.list(NOTEBOOK, image)
        cpu_skus, gpu_skus = plans["CPU"], plans["GPU"]
        plans_table = PrettyTable()
        plans_table.field_names = ['name', 'series', 'cpu', 'gpu', 'memory',
                                   'sku_item_price_id', 'sku_type', 'committed_days', 'unit_price']
        self.insert_plans_in_table(cpu_skus, plans_table)
        self.insert_plans_in_table(gpu_skus, plans_table)
        return plans, plans_table

    def insert_plans_in_table(self, skus_collection, plans_table):
        for sku in skus_collection:
            for sku_item_price in sku["plans"]:
                if not sku["is_free"]:
                    plans_table.add_row([sku['name'], sku['series'], sku['cpu'], sku['gpu'], sku['memory'],
                                        sku_item_price['sku_item_price_id'], sku_item_price['sku_type'], sku_item_price['committed_days'], sku_item_price['unit_price']])

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
