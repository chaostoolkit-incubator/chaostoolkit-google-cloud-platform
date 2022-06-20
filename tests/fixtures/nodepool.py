# -*- coding: utf-8 -*-

body = {
    "config": {
        "oauth_scopes": [
            "gke-version-default",
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/trace.append",
        ]
    },
    "initial_node_count": 3,
    "name": "default-pool",
}
