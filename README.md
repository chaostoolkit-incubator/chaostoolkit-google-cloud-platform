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
    "configuration": {
        "gcp_project_id": "...",
        "gcp_region": "..."
    },
    "method": [
        {
            "name": "create-cloud-run-service",
            "type": "action",
            "provider": {
                "type": "python",
                "module": "chaosgcp.cloudrun.actions",
                "func": "create_service",
                "arguments": {
                    "project_id": "...",
                    "region": "europe-west2",
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
                "arguments": {
                    "project_id": "...",
                    "region": "europe-west2",
                    "name": "demo"
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

All operations in this extension expect to know about the target project
and, almost always, the region as well. These can be provided in two
ways.

1. Each action or probe takes a `project_id` and `region` arguments
2. For some activities, you can also set the `parent` argument which looks like `projects/<ID>/locations/</region>`. This is equivalent to the previous approach so it's a matter of taste
3. You can pass the context via the `configuration` section of your experiment:

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

Note that the arguments will always take precedence over the configuration.

You always need to set at least the `project_id` either with the
configuration block (when it's the same project for all activities in the
experiment) or on each activity directly. This is because the extension
cannot always infer these from the credentials and therefore doesn't
attempt to.

### Credentials

This extension allows you to reuse the authentication available to whichever
user you are logged in on the machine running the experiment. In such case,
the extension delegates the lookup of the appropriate credentials to the
underlying
[GCP Python client](https://googleapis.dev/python/google-api-core/latest/auth.html).

In addition, the extension allows you to provide a [service account][sa] with
enough permissions to perform its operations.

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


Finally, the embedded way looks like this (it should rarely be needed and avoided):


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
