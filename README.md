<h2 align="center">
  <br>
  <p align="center"><img src="https://avatars.githubusercontent.com/u/32068152?s=200&v=4"></p>
</h2>

<h4 align="center">Google Cloud Platform Extension for the Chaos Toolkit</h4>

<p align="center">
   <a href="https://pypi.org/project/chaostoolkit-google-cloud-platform/">
   <img alt="Release" src="https://img.shields.io/pypi/v/chaostoolkit-google-cloud-platform.svg">
   <a href="#">
   <img alt="Build" src="https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/actions/workflows/build.yaml/badge.svg">
   <a href="https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/issues">
   <img alt="GitHub issues" src="https://img.shields.io/github/issues/chaostoolkit-incubator/chaostoolkit-google-cloud-platform?style=flat-square&logo=github&logoColor=white">
   <a href="https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/blob/master/LICENSE.md">
   <img alt="License" src="https://img.shields.io/github/license/chaostoolkit-incubator/chaostoolkit-google-cloud-platform">
   <a href="#">
   <img alt="Python version" src="https://img.shields.io/pypi/pyversions/chaostoolkit-google-cloud-platform.svg">
   <a href="https://pkg.go.dev/github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform">
</p>

<p align="center">
  <a href="https://join.slack.com/t/chaostoolkit/shared_invite/zt-22c5isqi9-3YjYzucVTNFFVIG~Kzns8g">Community</a> •
  <a href="https://github.com/chaostoolkit-incubator/chaostoolkit-google-cloud-platform/blob/master/CHANGELOG.md">ChangeLog</a>
</p>

---

Welcome to the Google Cloud Platform (GCP) extension for Chaos Toolkit. The
package aggregates activities to target your GCP projects and explore
your resilience via Chaos Engineering experiments.

## Install

This package requires Python 3.8+

To be used from your experiment, this package must be installed in the Python
environment where Chaos Toolkit already lives.

```
$ pip install -U chaostoolkit-google-cloud-platform
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
  "version": "1.0.0",
  "title": "Our users should not be impacted by increased latency from our services",
  "description": "Use traffic shaping from the load Balancer to explore the impact of latency on our users",
  "method": [
    {
      "name": "add-delay-to-traffic",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.lb.actions",
        "func": "inject_traffic_delay",
        "arguments": {
          "url_map": "my-service",
          "target_name": "all-paths",
          "target_path": "/*",
          "delay_in_seconds": 1,
          "impacted_percentage": 80
        }
      },
      "pauses": {
        "after": 180
      }
    }
  ],
  "rollbacks": [
    {
      "name": "remove-traffic-delay",
      "type": "action",
      "provider": {
        "type": "python",
        "module": "chaosgcp.lb.actions",
        "func": "remove_fault_injection_traffic_policy",
        "arguments": {
          "url_map": "my-service",
          "target_name": "all-paths",
          "target_path": "/*"
        }
      }
    }
  ]
}
```

That's it! You can now run it as `chaos run experiment.json`

Please explore the code to see existing probes and actions.

The extension picks up the credentials found on the machine running the
experiment as describe in the official
[Python GCP client](https://googleapis.dev/python/google-api-core/latest/auth.html).


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

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. You will need to install [PDM](https://pdm-project.org).

```console
$ pdm install --dev
```

Whenever you need to make contribution, ensure to run the linter as follows:

```console
$ pdm run format
$ pdm run lint
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pdm run test
```
