import string
import random


def get_random_string(N):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))


def cpu_plan_short_code(sku):
    return f"{sku.get('series')}-{sku.get('sku_type').split('-')[0]}-{sku.get('cpu')}-" \
           f"{sku.get('memory')}-{sku.get('gpu') if sku.get('gpu') else 0}"


def gpu_plan_short_code(sku):
    return f"{sku.get('series')}-{sku.get('sku_type').split('.')[1]}-{sku.get('cpu')}-" \
           f"{sku.get('memory')}-{sku.get('gpu') if sku.get('gpu') else 0}"


def plan_to_sku_id(skus, plan):
    if plan.startswith("CPU"):
        for sku in skus["CPU"]:
            if cpu_plan_short_code(sku) == plan:
                return sku.get("sku_id")
    else:
        for sku in skus["GPU"]:
            if gpu_plan_short_code(sku) == plan:
                return sku.get("sku_id")
    return False


def plan_name_to_sku_item_price_id(skus, sku_unique_name):
    if sku_unique_name.startswith("CPU"):
        for sku in skus["CPU"]:
            if not sku["is_free"] and cpu_plan_short_code(sku) == sku_unique_name:
                for plan in sku["plans"]:
                    if plan["committed_days"] == 0:
                        return plan.get("sku_item_price_id")
    else:
        for sku in skus["GPU"]:
            if not sku["is_free"] and gpu_plan_short_code(sku) == sku_unique_name:
                for plan in sku["plans"]:
                    if plan["committed_days"] == 0:
                        return plan.get("sku_item_price_id")
    return False
