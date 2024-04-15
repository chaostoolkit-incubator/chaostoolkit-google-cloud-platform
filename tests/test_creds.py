# -*- coding: utf-8 -*-

import fixtures

from chaosgcp import get_context


def test_context_from_config():
    ctx = get_context(fixtures.configuration)
    assert ctx.project_id == fixtures.configuration["gcp_project_id"]
    assert ctx.zone == fixtures.configuration["gcp_zone"]
    assert ctx.region == fixtures.configuration["gcp_region"]
    assert ctx.cluster_name == fixtures.configuration["gcp_gke_cluster_name"]


def test_context_default_values():
    """alllow for optional keys in the configuration with None as default"""
    ctx = get_context({})
    assert ctx.project_id is None
    assert ctx.zone is None
    assert ctx.cluster_name is None
    assert ctx.region is None


def test_context_use_params_values():
    """alllow for optional keys in the configuration with None as default"""
    ctx = get_context(
        fixtures.configuration, project_id="1234", region="region", zone="zone1"
    )
    assert ctx.project_id == "1234"
    assert ctx.zone == "zone1"
    assert ctx.cluster_name is fixtures.configuration["gcp_gke_cluster_name"]
    assert ctx.region == "region"
