# -*- coding: utf-8 -*-

import fixtures

from chaosgcp import get_context


def test_context_from_config():
    ctx = get_context(fixtures.configuration, fixtures.secrets)
    assert ctx.project_id == fixtures.configuration["gcp_project_id"]
    assert ctx.zone == fixtures.configuration["gcp_zone"]
    assert ctx.region == fixtures.configuration["gcp_region"]
    assert ctx.cluster_name == fixtures.configuration["gcp_gke_cluster_name"]


def test_context_default_values():
    """alllow for optional keys in the configuration with None as default"""
    ctx = get_context({}, fixtures.secrets)
    assert ctx.project_id is None
    assert ctx.zone is None
    assert ctx.cluster_name is None
    assert ctx.region is None
