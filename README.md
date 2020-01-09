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

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-google-cloud-platform
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "swap-nodepool-for-a-new-one",
    "provider": {
        "type": "python",
        "module": "chaosgcp.gke.nodepool.actions",
        "func": "swap_nodepool",
        "secrets": ["gcp", "k8s"],
        "arguments": {
            "old_node_pool_id": "...",
            "new_nodepool_body": {
                "nodePool": {
                    "config": { 
                        "oauthScopes": [
                            "gke-version-default",
                            "https://www.googleapis.com/auth/devstorage.read_only",
                            "https://www.googleapis.com/auth/logging.write",
                            "https://www.googleapis.com/auth/monitoring",
                            "https://www.googleapis.com/auth/service.management.readonly",
                            "https://www.googleapis.com/auth/servicecontrol",
                            "https://www.googleapis.com/auth/trace.append"
                        ]
                    },
                    "initialNodeCount": 3,
                    "name": "new-default-pool"
                }
            }
        }
    }
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

Note that most functions exposed in this package also take those values
directly when you want specific values for them.

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

While the embedded way looks like this:


```json
{
    "secrets": {
        "k8s": {
            "KUBERNETES_CONTEXT": "gke_project_name-g70e8ya0_us-central1_cluster-hello-world"
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

Here is a full example:

```json
{
    "version": "1.0.0",
    "title": "...",
    "description": "...",
    "configuration": {
        "gcp_project_id": "...",
        "gcp_gke_cluster_name": "...",
        "gcp_region": "...",
        "gcp_zone": "..."
    },
    "secrets": {
        "gcp": {
            "service_account_file": "/path/to/sa.json"
        },
        "k8s": {
            "KUBERNETES_CONTEXT": "gke_project_name-g70e8ya0_us-central1_cluster-hello-world"
        },
    },
    "method": [
        {
            "type": "action",
            "name": "swap-nodepool-for-a-new-one",
            "provider": {
                "type": "python",
                "module": "chaosgcp.gke.nodepool.actions",
                "func": "swap_nodepool",
                "secrets": ["gcp", "k8s"],
                "arguments": {
                    "old_node_pool_id": "...",
                    "new_nodepool_body": {
                        "nodePool": {
                            "config": { 
                                "oauthScopes": [
                                    "gke-version-default",
                                    "https://www.googleapis.com/auth/devstorage.read_only",
                                    "https://www.googleapis.com/auth/logging.write",
                                    "https://www.googleapis.com/auth/monitoring",
                                    "https://www.googleapis.com/auth/service.management.readonly",
                                    "https://www.googleapis.com/auth/servicecontrol",
                                    "https://www.googleapis.com/auth/trace.append"
                                ]
                            },
                            "initialNodeCount": 3,
                            "name": "new-default-pool"
                        }
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
