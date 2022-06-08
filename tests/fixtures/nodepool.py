# -*- coding: utf-8 -*-

body = {
    "nodePool": {
        "config": {
            "oauthScopes": [
                "gke-version-default",
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/logging.write",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/service.management.readonly",
                "https://www.googleapis.com/auth/servicecontrol",
                "https://www.googleapis.com/auth/trace.append",
            ]
        },
        "initialNodeCount": 3,
        "name": "default-pool",
    }
}
