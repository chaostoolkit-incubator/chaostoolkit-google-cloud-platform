# Chaos Toolkit Extension for Google Cloud Platform

[![Build Status](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform.svg?branch=master)](https://travis-ci.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-google-cloud-platform.svg)](https://www.python.org/)

This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the
[Google Cloud Platform][gcp].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org
[gce]: https://cloud.google.com/compute/
[gcp]: https://cloud.google.com


## Install

This package requires Python 3.7+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install --prefer-binary -U chaostoolkit-google-cloud-platform
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "version": "1.0.0",
    "title": "create and delete a cloud run service",
    "description": "n/a",
    "secrets": {
        "gcp": {
            "service_account_file": "service_account.json"
        }
    },
    "method": [
        {
            "name": "create-cloud-run-service",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.cloudrun.actions",
                "func": "create_service",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/...",
                    "service_id": "demo",
                    "container": {
                        "name": "demo",
                        "image": "gcr.io/google-samples/hello-app:1.0"
                    }
                }
            }
        },
        {
            "name": "delete-cloud-run-service",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.cloudrun.actions",
                "func": "delete_service",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/.../services/demo"
                }
            }
        }
    ]
}
```

That's it!

Please explore the code to see existing probes and actions.


## Configuration

### Project and Cluster Information

You can pass the context via the `configuration` section of your experiment:

```json
{
    "configuration": {
        "gcp_project_id": "...",
        "gcp_gke_cluster_name": "...",
        "gcp_region": "...",
        "gcp_zone": "..."
    }
}
```

This is only valuable when you want to reuse the same context everywhere.
A finer approach is to set the the `parent` argument on activities that
support it. It should be of the form
`projects/*/locations/*` or `projects/*/locations/*/clusters/*`, where
`location` is either a region or a zone, depending on the context and defined
by the GCP API.

When provided, this takes precedence over the context defined in the
configuration. In some cases, it also means you do not need to pass the
values in the configuration at all as the extension will derive the
context from the `parent` value.

### Credentials

This extension expects a [service account][sa] with enough permissions to
perform its operations. Please create such a service account manually (do not
use the default one for your cluster if you can, so you'll be able to delete
that service account if need be).

[sa]: https://cloud.google.com/iam/docs/creating-managing-service-accounts 

Once you have created your service account, either keep the file on the same
machine where you will be running the experiment from. Or, pass its content
as part of the `secrets` section, although this is not recommended because your
sensitive data will be quite visible.

Here is the first way:

```json
{
    "secrets": {
        "gcp": {
            "service_account_file": "/path/to/sa.json"
        }
    }
}
```

You can also use the well-known `GOOGLE_APPLICATION_CREDENTIALS` environment
variables. iI that case, you do not need to set any secrets in the
experiment.


While the embedded way looks like this:


```json
{
    "secrets": {
        "k8s": {
            "KUBERNETES_CONTEXT": "..."
        },
        "gcp": {
            "service_account_info": {
                "type": "service_account",
                "project_id": "...",
                "private_key_id": "...",
                "private_key": "...",
                "client_email": "...",
                "client_id": "...",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...."
            }
        }
    }
}
```

Notice also how we provided here the `k8s` entry. This is only because, in our
example we use the `swap_nodepool` action which drains the Kubernetes nodes
and it requires the Kubernetes cluster credentials to work. These are documented
in the [Kubernetes extension for Chaos Toolkit][k8sctk]. This is the only
action that requires such a secret payload, others only speak to the GCP API.

[k8sctk]: https://docs.chaostoolkit.org/drivers/kubernetes/

### Putting it all together

Here is a full example which creates a node pool then swap it for a new one.

```json
{
    "version": "1.0.0",
    "title": "do stuff ye",
    "description": "n/a",
    "secrets": {
        "k8s": {
            "KUBERNETES_CONTEXT": "gke_..."
        },
        "gcp": {
            "service_account_file": "service-account.json"
        }
    },
    "method": [
        {
            "name": "create-our-nodepool",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.actions",
                "func": "create_new_nodepool",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/.../clusters/...",
                    "body": {
                        "config": { 
                            "oauth_scopes": [
                                "gke-version-default",
                                "https://www.googleapis.com/auth/devstorage.read_only",
                                "https://www.googleapis.com/auth/logging.write",
                                "https://www.googleapis.com/auth/monitoring",
                                "https://www.googleapis.com/auth/service.management.readonly",
                                "https://www.googleapis.com/auth/servicecontrol",
                                "https://www.googleapis.com/auth/trace.append"
                            ]
                        },
                        "initial_node_count": 1,
                        "name": "default-pool"
                    }
                }
            }
        },
        {
            "name": "fetch-our-nodepool",
            "type": "probe",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.probes",
                "func": "get_nodepool",
                "secrets": ["gcp"],
                "arguments": {
                    "parent": "projects/.../locations/.../clusters/.../nodePools/default-pool"
                }
            }
        },
        {
            "name": "swap-our-nodepool",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.actions",
                "func": "swap_nodepool",
                "secrets": ["gcp", "k8s"],
                "arguments": {
                    "parent": "projects/.../locations/.../clusters/...",
                    "delete_old_node_pool": true,
                    "old_node_pool_id": "default-pool",
                    "new_nodepool_body": {
                        "config": { 
                            "oauth_scopes": [
                                "gke-version-default",
                                "https://www.googleapis.com/auth/devstorage.read_only",
                                "https://www.googleapis.com/auth/logging.write",
                                "https://www.googleapis.com/auth/monitoring",
                                "https://www.googleapis.com/auth/service.management.readonly",
                                "https://www.googleapis.com/auth/servicecontrol",
                                "https://www.googleapis.com/auth/trace.append"
                            ]
                        },
                        "initial_node_count": 1,
                        "name": "default-pool-1"
                    }
                }
            }
        }
    ]
}
```


## Migrate from GCE extension

If you previously used the deprecated [GCE extension][ctk-gce], here is a quick
recap of changes you'll need to go through to update your experiments.

[ctk-gce]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud

-   The module `chaosgce.nodepool.actions` has been replaced by
    `chaosgcp.gke.nodepool.actions`.
    You will need to update the `module` key for the python providers.
-   The configuration keys in the `configuration` section have been
    renamed accordingly:
    - `"gce_project_id"` -> `"gcp_project_id"`
    - `"gce_region"` -> `"gcp_region"`
    - `"gce_zone"` -> `"gcp_zone"`
    - `"gce_cluster_name"` -> `"gcp_gke_cluster_name"`

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

If you wish to add a new function to this extension, that is related to a 
Google Cloud product that is not available yet in this package, please use 
the product short name or acronym as a first level subpackage (eg. iam, gke, 
sql, storage, ...). See the list of [GCP products and services][gcp_products].

[gcp_products] https://cloud.google.com/products/

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
