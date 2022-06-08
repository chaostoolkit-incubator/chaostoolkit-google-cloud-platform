# -*- coding: utf-8 -*-
import copy

trigger = {
    "id": "1559987a-6302-4b11-b033-d6d06ef256c5",
    "createTime": "2020-02-27T08:22:25.894959516Z",
    "description": "This is an example of Cloud Build trigger",
    "substitutions": {},
    "github": {},
    "ignoredFiles": [],
    "includedFiles": ["cloudbuild.yaml"],
    "name": "a-dummy-trigger",
    "filename": "cloudbuild.yaml",
}


triggers = {"triggers": [copy.deepcopy(trigger)]}

triggered_build = {
    "name": "operations/build/chaosiqdemos/NTU4Y2JlM2EtMTFkNC00MWZlLWEzZGEtNGY3Yzk4NDliNTkx",  # noqa
    "metadata": {
        "@type": "type.googleapis.com/google.devtools.cloudbuild.v1.BuildOperationMetadata",  # noqa
        "build": {
            "id": "558cbe3a-11d4-41fe-a3da-4f7c9849b591",
            "status": "QUEUED",
        },
    },
}
