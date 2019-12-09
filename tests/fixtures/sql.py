# -*- coding: utf-8 -*-

instances = [
    {
    "kind": "sql#instance",
    "state": "RUNNABLE",
    "databaseVersion": "POSTGRES_11",
    "settings": {
        "authorizedGaeApplications": [],
        "tier": "db-g1-small",
        "kind": "sql#settings",
        "availabilityType": "REGIONAL",
        "pricingPlan": "PER_USE",
        "replicationType": "SYNCHRONOUS",
        "activationPolicy": "ALWAYS",
        "ipConfiguration": {
            "authorizedNetworks": [],
            "ipv4Enabled": True,
            "requireSsl": True
        },
        "locationPreference": {
            "zone": "us-central1-a",
            "kind": "sql#locationPreference"
        },
        "dataDiskType": "PD_SSD",
        "maintenanceWindow": {
            "updateTrack": "stable",
            "kind": "sql#maintenanceWindow",
            "hour": 14,
            "day": 7
        },
        "backupConfiguration": {
            "startTime": "07:00",
            "kind": "sql#backupConfiguration",
            "enabled": True
        },
        "settingsVersion": "21",
        "storageAutoResizeLimit": "0",
        "storageAutoResize": True,
        "dataDiskSizeGb": "10"
    },
    "etag": "dd96062609a55c83f67983d6b938a326bd7364390440e6ab24347815eea86d1b",
    "failoverReplica": {
        "available": True
    },
    "ipAddresses": [
        {
            "type": "PRIMARY",
            "ipAddress": "35.224.10.25"
        }
    ],
    "instanceType": "CLOUD_SQL_INSTANCE",
    "project": "chaosiqdemos",
    "backendType": "SECOND_GEN",
    "name": "pgsql-20191115184040913900000001",
    "region": "us-central1",
    "gceZone": "us-central1-a"
    }
]


failover_body = {
    "failoverContext": {
        "kind": "sql#failoverContext",
        "settingsVersion": "21"
    }
}


failover_operation = {
    "kind": "sql#operation",
    "status": "DONE",
    "insertTime": "2019-11-29T15:10:50.874Z",
    "startTime": "2019-11-29T15:10:51.098Z",
    "endTime": "2019-11-29T15:11:21.026Z",
    "operationType": "FAILOVER",
    "name": "mysqlfailover",
    "targetId": "pgsql-20191115184040913900000001",
    "targetProject": "chaosiqdemos",
}
