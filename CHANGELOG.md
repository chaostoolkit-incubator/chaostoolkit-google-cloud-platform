# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.12.3...HEAD

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
