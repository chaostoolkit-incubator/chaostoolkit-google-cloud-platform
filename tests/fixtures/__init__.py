# -*- coding: utf-8 -*-
from fixtures import cloudbuild, cloudrun, nodepool, sql, storage  # noqa

secrets = {"service_account_file": "tests/fixtures/fake_creds.json"}

secrets_with_k8s = {
    "service_account_file": "tests/fixtures/fake_creds.json",
    "KUBERNETES_CONTEXT": "minikube",
}


configuration = {
    "gcp_project_id": "chaosiqdemos",
    "gcp_zone": "us-west1-a",
    "gcp_region": "us-west1",
    "gcp_gke_cluster_name": "demos-cluster",
}
