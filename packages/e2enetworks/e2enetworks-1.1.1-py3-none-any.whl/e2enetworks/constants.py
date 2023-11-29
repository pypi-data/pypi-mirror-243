MY_ACCOUNT_LB_URL = "https://api.e2enetworks.com/myaccount/"
GPU_URL = "api/v1/gpu/"
BASE_GPU_URL = f"{MY_ACCOUNT_LB_URL}{GPU_URL}"
VALIDATED_SUCCESSFULLY = "Validated Successfully"
INVALID_CREDENTIALS = "Validation Failed, Invalid APIkey or Token"
headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://thor-gpu.e2enetworks.net',
            'Referer': 'https://thor-gpu.e2enetworks.net/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        }
MANAGED_STORAGE = "managed"
E2E_OBJECT_STORAGE = "e2e_s3"
BUCKET_TYPES = [MANAGED_STORAGE, E2E_OBJECT_STORAGE]
BUCKET_TYPES_HELP = {
    MANAGED_STORAGE: "To Create New Bucket",
    E2E_OBJECT_STORAGE: " To Use Existing Bucket"
}
NOTEBOOK = "notebook"
INFERENCE = "inference_service"

FREE_USAGE = "free_usage"
PAID_USAGE = "paid_usage"
INSTANCE_TYPE = [FREE_USAGE, PAID_USAGE]
TRITON = "triton"
PYTORCH = "pytorch"
MODEL_TYPES = ['pytorch', 'triton', 'custom']
S3_ENDPOINT = "objectstore.e2enetworks.net"
