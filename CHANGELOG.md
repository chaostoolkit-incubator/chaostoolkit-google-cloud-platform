# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/compare/0.4.0...HEAD

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
