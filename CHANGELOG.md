# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/tree/HEAD

## [0.1.0][] - 2019-12-11

[0.1.0]: https://github.com/chaostoolkit/chaostoolkit-google-cloud-platform/tree/0.1.0

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
