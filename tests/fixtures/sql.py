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
                "requireSsl": True,
            },
            "locationPreference": {
                "zone": "us-central1-a",
                "kind": "sql#locationPreference",
            },
            "dataDiskType": "PD_SSD",
            "maintenanceWindow": {
                "updateTrack": "stable",
                "kind": "sql#maintenanceWindow",
                "hour": 14,
                "day": 7,
            },
            "backupConfiguration": {
                "startTime": "07:00",
                "kind": "sql#backupConfiguration",
                "enabled": True,
            },
            "settingsVersion": "21",
            "storageAutoResizeLimit": "0",
            "storageAutoResize": True,
            "dataDiskSizeGb": "10",
        },
        "etag": "dd96062609a55c83f67983d6b938a326bd7364390440e6ab24347815eea86d1b",  # noqa
        "failoverReplica": {"available": True},
        "ipAddresses": [{"type": "PRIMARY", "ipAddress": "35.224.10.25"}],
        "instanceType": "CLOUD_SQL_INSTANCE",
        "project": "chaosiqdemos",
        "backendType": "SECOND_GEN",
        "name": "pgsql-20191115184040913900000001",
        "region": "us-central1",
        "gceZone": "us-central1-a",
    }
]


failover_body = {
    "failoverContext": {"kind": "sql#failoverContext", "settingsVersion": "21"}
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


sql_operation_done = {
    "kind": "sql#operation",
    "name": "mysqloperation",
    "status": "DONE",
    "error": {},
}


export_operation = {
    "kind": "sql#operation",
    "status": "DONE",
    "insertTime": "2019-12-10T15:16:04.381Z",
    "startTime": "2019-12-10T15:16:04.661Z",
    "endTime": "2019-12-10T15:16:15.045Z",
    "operationType": "EXPORT",
    "exportContext": {
        "uri": "gs://chaosiqdemos/dump.sql",
        "databases": ["demo"],
        "kind": "sql#exportContext",
        "sqlExportOptions": {
            "schemaOnly": False,
            "mysqlExportOptions": {"masterData": 0},
        },
        "fileType": "SQL",
    },
    "name": "mysqlexport",
    "targetId": "pgsql-20191115184040913900000001",
    "targetProject": "chaosiqdemos",
}


import_operation = {
    "kind": "sql#operation",
    "status": "DONE",
    "insertTime": "2019-12-10T15:16:17.240Z",
    "startTime": "2019-12-10T15:16:17.449Z",
    "endTime": "2019-12-10T15:16:27.767Z",
    "error": {},
    "operationType": "IMPORT",
    "importContext": {
        "uri": "gs://chaosiqdemos/dump.sql",
        "database": "demo",
        "kind": "sql#importContext",
        "fileType": "SQL",
        "importUser": "chaosiq",
    },
    "name": "mysqlimport",
    "targetId": "pgsql-20191115184040913900000001",
    "targetProject": "chaosiqdemos",
}


databases = [
    {
        "kind": "sql#database",
        "charset": "UTF8",
        "collation": "en_US.UTF8",
        "etag": "a797327e6265f5966f4995432791ab6cfdb09f47557d9339c0cef99a1ff3a011",  # noqa
        "name": "postgres",
        "instance": "pgsql-20191115184040913900000001",
        "project": "chaosiqdemos",
    },
    {
        "kind": "sql#database",
        "charset": "UTF8",
        "collation": "en_US.UTF8",
        "etag": "b905ba0bc656c7b4621d7733ea72f0b325f6e68c1f57ea1bd393aa3112ac9b1b",  # noqa
        "name": "chaos",
        "instance": "pgsql-20191115184040913900000001",
        "project": "chaosiqdemos",
    },
]
