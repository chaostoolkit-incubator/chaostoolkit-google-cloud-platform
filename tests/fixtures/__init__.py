"""

This file is where all the configuration values for all the resources needed for running tests in test files.

"""
# -*- coding: utf-8 -*-
from fixtures import cloudbuild
from fixtures import cloudrun
from fixtures import dns
from fixtures import nodepool
from fixtures import sql
from fixtures import storage

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
