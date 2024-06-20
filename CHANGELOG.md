# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.32.1...HEAD

### Changed

* Always return falsey from `chaosgcp.monitoring.proves.valid_slo_ratio_during_window`
  when no data was found for the SLO
* Bump dependencies

## [0.32.1][] - 2024-05-31

[0.32.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.32.0...0.32.1

### Fixed

* Convert string to int. GCP returns int64 as a string to let the client to make
  the decision how to convert it. Python doesn't differentiate explicitely so we
  are left to let the Python VM make the right decision for us

## [0.32.0][] - 2024-05-31

[0.32.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.31.0...0.32.0

### Added

* Support for more typed value when verifying SLO with
  `valid_slo_ratio_during_window`

## [0.31.0][] - 2024-05-28

[0.31.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.30.1...0.31.0

### Changed

* Removed unusued `(` character
* Refactored code to locate the appropriate target

## [0.30.1][] - 2024-05-28

[0.30.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.30.0...0.30.1

### Fixed

* Fixed returned type in `chaosgcp.lb.get_path_matcher`
* Fixed load balancer activities to use `target_path` where appropriate

## [0.30.0][] - 2024-05-28

[0.30.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.29.0...0.30.0

### Changed

* Support for route rules in `chaosgcp.lb` activities

## [0.29.0][] - 2024-05-27

[0.29.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.28.0...0.29.0

### Changed

* Make sure region and project can be passed to monitoring probes

## [0.28.0][] - 2024-05-24

[0.28.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.27.0...0.28.0

#### Added

* `suspend_vm_instance` and `resume_vm_instance` functions to 
* `chaosgcp.compute.actions`. These functions suspend a running
* GCE VM instance and resume any suspended GCE VM respectively.
* They can be called for action in experiments as follows:

  ```json
   {
	"name" : "Suspend VM",
	"type" : "action",
        "provider": {
            	"type": "python",
		        "module": "chaosgcp.compute.actions",
		        "func": "suspend_vm_instance",
                "arguments" : {
                    "project_id" : "prj-shared-ntwk-prod",
                    "zone" : "us-central1-b",
                    "instance_name" : "mig-exp-ig-24w1"
                }
            }
        }
* Added test cases for both the functions as well.
* Added the `chaosgcp.lb.probes.get_fault_injection_traffic_policy` probe

#### Changed

* Bumped dependencies

## [0.27.0][] - 2024-05-14

[0.27.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.26.0...0.27.0

#### Changed

* Drop `logzero` and use `logger = logging.getLOgger("chaostoolkit")` instead
* Bump dependencies

## [0.26.0][] - 2024-05-06

[0.26.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.25.0...0.26.0

#### Added

* The `chaosgcp.iam.controls.policy` control to Manage temporary, 
* time-bound IAM roles for the specified project and members.
* This controls grants specified IAM roles to the provided members,
* with an expiration time determined by the given expiry_time_in_minutes
* before experiment and revokes the specified IAM roles from the
* provided members after the experiment:

  ```json
    "controls": [
        {
  "name": "gcp-iampolicy-timebound",
  "provider": {
    "type": "python",
    "module": "chaosgcp.iam.controls.policy",
    "arguments": {
      "project_id":"myproject",
      "roles": ["roles/storage.admin"],
      "members": ["serviceAccount:dp-sa11@myproject.iam.gserviceaccount.com"],
      "expiry_time_in_minutes": 10
                }
            }
        }
    ]

## [0.25.0][] - 2024-04-30

[0.25.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.24.0...0.25.0

### Added

* The `chaosgcp.networkconnectivity.actions` activities to set policy based route

## [0.24.0][] - 2024-04-30

[0.24.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.23.0...0.24.0

### Added

* The `chaosgcp.compute.actions` activities to set tags on resources
* Ensuring actions return a response as per their signature

## [0.23.0][] - 2024-04-10

[0.23.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.22.0...0.23.0

### Added

* The `chaosgcp.dns.actions` activities to update a DNS record

## [0.22.0][] - 2024-03-27

[0.22.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.21.1...0.22.0

### Added

* The `chaosgcp.cloudlogging.controls.journal` control to send the journal
  to GCP Cloud Logging:

  ```json
  "controls": [
        {
            "name": "gcp-journal-logger",
            "provider": {
                "type": "python",
                "module": "chaosgcp.cloudlogging.controls.journal",
                "arguments": {
                    "labels": {
                        "appid": "123456"
                    }
                }
            }
        }
    ]
  ```

## [0.21.1][] - 2024-03-15

[0.21.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.21.0...0.21.1

### Fixed

* `get_backend_service_health` requires to be iterated over each network group

## [0.21.0][] - 2024-03-15

[0.21.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.20.1...0.21.0

### Added

* The `get_backend_service_health` probe in the load balancing package

## [0.20.1][] - 2024-03-15

[0.20.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.20.0...0.20.1

### Fixed

* Make sure `run_mql_query` returns the values it computed

## [0.20.0][] - 2024-03-14

[0.20.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.19.0...0.20.0

### Added

* The `run_mql_query` probe in the monitoring package

## [0.19.0][] - 2024-03-14

[0.19.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.18.1...0.19.0

### Changed

* Support string filters in `get_metrics`

## [0.18.1][] - 2024-03-14

[0.18.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.18.0...0.18.1

### Fixed

* Expose `chaosgcp.gke.nodepool.actions.resize_nodepool` action

## [0.18.0][] - 2024-03-14

[0.18.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.17.1...0.18.0

### Added

* The `chaosgcp.gke.nodepool.actions.resize_nodepool` action

### Changed

* Bump dependencies

## [0.17.1][] - 2024-03-08

[0.17.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.17.0...0.17.1

### Changed

* Bump dependencies

## [0.17.0][] - 2024-03-08

[0.17.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.17.0...0.17.0

### Changed

* Allow to retrieve the project id from the `GCP_PROJECT_ID` environment
  variable
* Bump dependencies

## [0.16.1][] - 2024-02-21

[0.16.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.16.0...0.16.1

### Fixed

* Remove trailing function call in monitoring/actions.py module

## [0.16.0][] - 2024-02-21

[0.16.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.15.0...0.16.0

### Changed

* Switched from `setuptools`to [pdm](https://pdm-project.org) to package and
  manage the project. This also brings a much stricter dependency management
  support
* Read package version using `importlib_metadata`
* Drops supports for Python 3.7 as it's been EOL since June 2023
* Adds Code of Conduct file

## [0.15.0][] - 2023-12-08

[0.15.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.14.1...0.15.0

### Changed

* All actions and probes now take optional `project_id` and `region` arguments
  so that they can be set on per activity basis. In that case, they take
  precedence over the configuration payload. But this also means, the configuration
  block can be left unset entirely for these fields
* It is not expected anymore that you set a service account file to authenticate
  When none is provided, we delegate to the GCP client library to figure it out.
  This allows for newer authentication approaches supported by that client
  without relying on a less secure service account

### Breaking

* In the `chaosgcp.cloudrun.probes.get_service` probe, the `name` argument has
  been repurposed and has been renamed to `parent`. The `name` now expects
  the service name without its parent path as a prefix.
* The extension will not raise an `ActivityFailed` exception when it could not
  load credentials explicitely set from the secrets. This is so the underlying
  client can attempt to load credentials directly and natively

## [0.14.1][] - 2023-10-24

[0.14.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.14.0...0.14.1

### Fixed

* Read region from the configuration block in the load balancer actions

## [0.14.0][] - 2023-10-24

[0.14.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.13.2...0.14.0

### Added

* Network Endpoint Groups actions and probes

## [0.13.2][] - 2023-10-24

[0.13.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.13.1...0.13.2

### Fixed

* Set the `region` paramater in LB requests

## [0.13.1][] - 2023-10-11

[0.13.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.13.0...0.13.1

### Changed

* renamed `service_has_at_least_slo_across_time` to `valid_slo_ratio_during_window`

## [0.13.0][] - 2023-10-11

[0.13.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.12.3...0.13.0

### Added

* the `service_has_at_least_slo_across_time` probe to use in a steady-state

## [0.12.3][] - 2023-10-09

[0.12.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.12.2...0.12.3

### Changed

* Make `get_slo_health` `cross_series_reducer` and per_series_aligner arguments
  are now strings and mapped back to their numeric value as it's friendlier that
  way

## [0.12.2][] - 2023-10-09

[0.12.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.12.1...0.12.2

### Changed

* Make `get_slo_health` `group_by_fields` argument support comma-separated strings

## [0.12.1][] - 2023-10-09

[0.12.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.12.0...0.12.1

### Changed

* Removed unused argument in `get_slo_budget`
* Fix types for `per_series_aligner` and `cross_series_reducer` in `get_slo_health`

## [0.12.0][] - 2023-10-09

[0.12.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.11.0...0.12.0

### Added

* Support for regional LB access from the load-balancer actions
* SLO probes

## [0.11.0][] - 2023-08-23

[0.11.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.10.1...0.11.0

### Added

* Also read credentials from `GCP_APPLICATION_CREDENTIALS` as an alternative to
  `GOOGLE_APPLICATION_CREDENTIALS` since the latter can lead to issues when
  running in GCP Cloud Run job which already provides its own credentials

## [0.10.1][] - 2023-08-22

[0.10.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.10.0...0.10.1

### Fixed

* Added missing compute dependency

## [0.10.0][] - 2023-08-22

[0.10.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.9.2...0.10.0

### Added

* Added fault injection policiy actions for UrlMap/LB

### Changed

* Switched from flake8 to ruff

## [0.9.2][] - 2023-05-18

[0.9.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.9.0...0.9.2

### Changed

* Fixed missing dependencies

## [0.9.0][] - 2023-05-18

[0.9.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.8.2...0.9.0

### Added

* Probes to list docker images and their vulnerabilities from Artifact Registry

## [0.8.2][] - 2023-02-08

[0.8.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.8.1...0.8.2

### Changed

* Default first on secret before env variable

## [0.8.1][] - 2023-02-08

[0.8.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.8.0...0.8.1

### Fixed

* Missing dependencies on in setup file

## [0.8.0][] - 2023-02-07

[0.8.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.7.0...0.8.0

### Added

- A `get_metrics` probe to query Cloud Monitoring data
- A `get_logs_between_timestamps` probe to query Cloud Logging data

## [0.7.0][] - 2023-02-01

[0.7.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.6.0...0.7.0


### Added

- Support for `GOOGLE_APPLICATION_CREDENTIALS` as the default way to authenticate

## [0.6.0][] - 2023-02-01

[0.6.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.5.0...0.6.0

### Added

- A `restore_backup` action to restore Cloud SQL backups
- A `promote_replica` action to promote a read replica to a standalone instance
- A `enable_replication` action to enable replication on a a read replica
- A `disable_replication` action to disable replication on a a read replica

### Changed
- Renamed field max_instance_request_concurrency in create_service method. Modified init value.
- Added vpc_access parameter to RevisionTemplate object
- Added test for 'chaosgcp.cloudrun.actions.update_service'
- Updated RevisionTemplate field name max_instance_request_concurrency
- Updated Cloud SQL activities to the `v1` API


## [0.5.0][] - 2022-06-21

[0.5.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.4.1...0.5.0

### Changed

[CAUTION]: We took care of not breaking compatibility but please report if you
have a changed behavior with this version!

- Fix discover between probes and actions
- Migrated to newer gcp Python client 
- Introducing support for the `parent` argument to locate resources

## [0.4.1][] - 2022-06-14

[0.4.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.4.0...0.4.1

### Changed

- Expose `chaosgcp.nodepool.actions.rollback` through the `dicover` interface

## [0.4.0][] - 2022-06-14

[0.4.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.3.0...0.4.0

### Added

- `chaosgcp.nodepool.probes` to `list` and `get` nodepools of a cluster
- `chaosgcp.nodepool.actions.rollback` when the upgrade of nodepool failed

## [0.3.0][] - 2022-06-08

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.2.1...0.3.0

### Added

- `chaosgcp.cloudrun` package for Cloud Run support

### Changed

- Switched from travis to github actions

## [0.2.1][] - 2020-04-30

[0.2.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.2.0...0.2.1

### Added

-   `chaosgcp.cloudbuild` package is embedded into distributed source package;
    it was missing from previous 0.2.0 release.

### Changed

-   Allow discovering probes & actions from `chaosgcp.cloudbuld` package

## [0.2.0][] - 2020-04-30

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.1.0...0.2.0

### Added

-   New probes for listing and describing instance databases in
    `chaosgcp.sql.probes` module: `list_databases`and `describe_database`.
-   New `chaosgcp.cloudbuild` package for Google Cloud Build probes and actions.
    List, retrieve and run cloud build triggers.
    
### Changed

-   Pass the secrets to the `drain_nodes` action, that is called in the
    `swap_nodepool` action, so that it knows how to connect to the Kubernetes
    cluster to be drained. [#9][9]

[#9]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/issues/9

## [0.1.0][] - 2019-12-11

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/tree/0.1.0

### Added

-   Initial release
    This extension has the following internal structure:
    ``chaosgcp`` package with GCP products as first level subpackage.
    This structure intends to follow GCP products navigation, as seen
    on the GCP console to keep some consistency for the user.
-   New `chaosgcp.gke` package for Google Kubernetes Engine probes & actions.
-   New `chaosgcp.sql` package for Google Cloud SQL probes and actions.
-   New `chaosgcp.storage` package for Google Cloud Storage probes and actions.

### Changed

-   The `chaosgce.nodepool` package from the deprecated 
    `chaostoolkit-google-cloud` extension has been ported to
     `chaosgcp.gke.nodepool`.
-   Allow optional values in GCPContext
-   Refactored wait_on_operation to accept multiple & various keyword arguments
-   Expose a load_credentials function in `chaosgcp` to load credentials
    from secrets.

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.22.0...HEAD

### Added

* DNS action to patch record sets
