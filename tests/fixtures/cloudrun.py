containers = {"image": "gcr.io/cloudrun/hello"}

max_instances: int = 100

service_account = "12345-dummy@developer.gserviceaccount.com"

encryption_key = (None,)

traffics = [
    {"type_": 1, "percent": 10},
    {"type_": 2, "revision": "dummy-12345", "percent": 90},
]

labels = (None,)

vpc_access = {
    "connector": "projects/myproject/locations/../connectors/foo-vpc-connector",
    "egress": "ALL_TRAFFIC",
}

template = {
    "service_account": f"{service_account}",
    "containers": {"image": "gcr.io/cloudrun/hello"},
    "max_instance_request_concurrency": f"{max_instances}",
}
