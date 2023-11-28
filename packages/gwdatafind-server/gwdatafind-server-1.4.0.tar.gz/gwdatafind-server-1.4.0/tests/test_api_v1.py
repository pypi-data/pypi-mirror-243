# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

from unittest import mock

import pytest

from gwdatafind_server.api import utils as api_utils

parametrize_routes = pytest.mark.parametrize("prefix", (
    pytest.param("/api", id="v1"),
    pytest.param("/services/data", id="ldr compat 1"),
    pytest.param("/LDR/services/data", id="ldr compat 2"),
))


# -- test API -------------------------

@parametrize_routes
def test_find_observatories(client, prefix):
    """Test the `find_observatories` view
    """
    resp = client.get(f"{prefix}/v1/gwf.json")
    assert resp.status_code == 200
    assert sorted(resp.json) == ["H", "L"]


@parametrize_routes
def test_find_observatories_error(client, prefix):
    """Test the `find_observatories` error response
    """
    resp = client.get(f"{prefix}/v1/bad.json")
    assert resp.status_code == 404, resp.json
    assert resp.json["message"] == "Filetype 'bad' not found"


@pytest.mark.parametrize(("obs", "types"), [
    ('L', ["L1_TEST_1", "L1_TEST_2"]),
    ('all', ["H1_TEST_1", "L1_TEST_1", "L1_TEST_2"]),
])
@parametrize_routes
def test_find_types(client, prefix, obs, types):
    """Test the `find_types` view
    """
    resp = client.get(f"{prefix}/v1/gwf/{obs}.json")
    assert resp.status_code == 200
    assert sorted(resp.json) == sorted(types)


@parametrize_routes
def test_find_types_error(client, prefix):
    """Test the `find_types` error response
    """
    resp = client.get(f"{prefix}/v1/gwf/bad.json")
    assert resp.status_code == 400, resp.json
    assert resp.json["message"] == "Observatory ID 'bad' not recognised"


@pytest.mark.parametrize('ext, segs', [
    ('gwf', [[1000000000, 1000000008], [1000000012, 1000000020]]),
    ('h5', [[1000000000, 1000000008]]),
])
@parametrize_routes
def test_find_times_all(client, prefix, ext, segs):
    """Test the `find_times` view without specifying limits
    """
    resp = client.get(f"{prefix}/v1/{ext}/L/L1_TEST_1/segments.json")
    assert resp.status_code == 200
    assert resp.json == segs


@parametrize_routes
def test_find_times(client, prefix):
    """Test the `find_times` view with limits
    """
    resp = client.get(
        f"{prefix}/v1/gwf/L/L1_TEST_1/segments/"
        "1000000007,1000000013.json",
    )
    assert resp.status_code == 200
    assert resp.json == [
        [1000000007, 1000000008],
        [1000000012, 1000000013],
    ]


@mock.patch.object(api_utils, "_DEFAULT_GSIFTP_HOST", new="testhost")
@parametrize_routes
def test_find_url(client, prefix):
    """Test the `find_url` view
    """
    resp = client.get(
        f"{prefix}/v1"
        "/h5/L/L1_TEST_1/L-L1_TEST_1-1000000000-4.h5.json",
    )
    assert resp.status_code == 200
    assert resp.json == [
        "file://localhost/test/path/L-L1_TEST_1-1000000000-4.h5",
        "gsiftp://testhost:15000/test/path/L-L1_TEST_1-1000000000-4.h5",
    ]


@mock.patch.object(api_utils, "_DEFAULT_GSIFTP_HOST", new="testhost")
@parametrize_routes
def test_find_urls(client, prefix):
    """Test the `find_urls` view with no special options
    """
    resp = client.get(
        f"{prefix}/v1/gwf/L/L1_TEST_1/1000000004,1000000016.json",
    )
    assert resp.status_code == 200
    assert sorted(resp.json) == [
        "file://localhost/test/path/L-L1_TEST_1-1000000004-4.gwf",
        "file://localhost/test/path2/L-L1_TEST_1-1000000012-4.gwf",
        "gsiftp://testhost:15000/test/path/L-L1_TEST_1-1000000004-4.gwf",
        "gsiftp://testhost:15000/test/path2/L-L1_TEST_1-1000000012-4.gwf",
    ]


@parametrize_routes
def test_find_urls_fancy(client, prefix):
    """Test the `find_urls` view with extra options
    """
    resp = client.get(
        f"{prefix}/v1"
        "/gwf/L/L1_TEST_1/1000000000,1000000008/file.json?match=04",
    )
    assert resp.status_code == 200
    assert sorted(resp.json) == [
        "file://localhost/test/path/L-L1_TEST_1-1000000004-4.gwf",
    ]


@parametrize_routes
def test_find_urls_filter_preference(client, prefix):
    """Test the `find_urls` view with `filter_preference`
    """
    resp = client.get(
        f"{prefix}/v1"
        "/h5/H/H1_TEST_1/1000000000,1000000004/file.json",
    )
    assert resp.status_code == 200
    assert sorted(resp.json) == [
        "file://localhost/test/preferred/path/H-H1_TEST_1-1000000000-8.h5",
    ]


@mock.patch.object(api_utils, "_DEFAULT_GSIFTP_HOST", new="testhost")
@pytest.mark.parametrize(("start", "end"), [
    (1000000003.5, 1000000012.5),
    (1000000003, 1000000012.5),
    (1000000003.5, 1000000013),
])
@parametrize_routes
def test_find_urls_noninteger(client, prefix, start, end):
    """Test the `find_urls` view with non-integer GPS times.
    """
    resp = client.get(
        f"{prefix}/v1/gwf/L/L1_TEST_1/{start},{end}.json",
    )
    assert resp.status_code == 200
    assert sorted(resp.json) == [
        "file://localhost/test/path/L-L1_TEST_1-1000000000-4.gwf",
        "file://localhost/test/path/L-L1_TEST_1-1000000004-4.gwf",
        "file://localhost/test/path2/L-L1_TEST_1-1000000012-4.gwf",
        "gsiftp://testhost:15000/test/path/L-L1_TEST_1-1000000000-4.gwf",
        "gsiftp://testhost:15000/test/path/L-L1_TEST_1-1000000004-4.gwf",
        "gsiftp://testhost:15000/test/path2/L-L1_TEST_1-1000000012-4.gwf",
    ]


def test_find_urls_osdf(client):
    """Check that paths get transformed into OSDF URLs appropriately.
    """
    resp = client.get(
        "/services/data/v1"
        "/gwf/H/H1_TEST_1/1000000000,1000000012/osdf.json",
    )
    assert resp.status_code == 200
    assert sorted(resp.json) == [
        "osdf:///export/igwn/test/H-H1_TEST_1-1000000008-4.gwf",
    ]


def test_find_urls_osdf_empty(client):
    """Check that URLS that don't support OSDF return empty.
    """
    resp = client.get(
        "/services/data/v1/gwf/L/L1_TEST_1/1000000004,1000000016/osdf.json",
    )
    assert resp.status_code == 200
    assert not resp.json  # no hits that support OSDF


@mock.patch.object(api_utils, "_DEFAULT_GSIFTP_HOST", new="testhost")
@parametrize_routes
def test_find_latest(client, prefix):
    """Test the `find_latest` view
    """
    resp = client.get(
        f"{prefix}/v1/gwf/L/L1_TEST_1/latest.json",
    )
    assert resp.status_code == 200
    assert resp.json == [
        "file://localhost/test/path2/L-L1_TEST_1-1000000016-4.gwf",
        "gsiftp://testhost:15000/test/path2/L-L1_TEST_1-1000000016-4.gwf",
    ]


@parametrize_routes
def test_find_latest_urltype(client, prefix):
    """Test the `find_latest` view with urltype
    """
    resp = client.get(
        f"{prefix}/v1/gwf/L/L1_TEST_1/latest/file.json",
    )
    assert resp.status_code == 200
    assert resp.json == [
        "file://localhost/test/path2/L-L1_TEST_1-1000000016-4.gwf",
    ]
