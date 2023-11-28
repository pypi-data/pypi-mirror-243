# -*- coding: utf-8 -*-
# Copyright (2023) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Tests for the :mod:`gwdatafind_server.cache` module.
"""

from pathlib import Path

import pytest

from ligo.segments import segment, segmentlist

from gwdatafind_server import cache

TEST_DIR = Path(__file__).parent

DISKCACHE_VERSION_MULTIPLE_EXTENSIONS = "0x0101"

# the cache, in full
CACHE = {
    'gwf': {
        'H': {
            'H1_TEST_1': {
                ('/test/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
                ('/cvmfs/h.storage.igwn.org/igwn/test', 4): segmentlist([
                    segment(1000000008, 1000000016),
                ])
            },
        },
        'L': {
            'L1_TEST_1': {
                ('/test/path2', 4): segmentlist([
                    segment(1000000012, 1000000020),
                ]),
                ('/test/path', 4): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
            'L1_TEST_2': {
                ('/test/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
            'L1_TEST_IGNORE': {
                ('/test/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
        },
        'X': {
            'X1_TEST_2': {
                ('/test/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
        },
        'Y': {
            'Y1_EXCLUDE_1': {
                ('/test/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
        },
    },
    'h5': {
        'H': {
            'H1_TEST_1': {
                ('/test/preferred/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
                ('/test/other/path', 8): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
        },
        'L': {
            'L1_TEST_1': {
                ('/test/path', 4): segmentlist([
                    segment(1000000000, 1000000008),
                ]),
            },
        },
    },
}


@pytest.mark.parametrize("cache_version", [
    "0x00ff",
    "0x0101",
])
def test_parse_diskcache_multiextension(app, cache_version):
    cache_file = TEST_DIR / f"cache-{cache_version}.dat"
    cacheman = cache.CacheManager(app, cache_file)
    cacheman.parse()
    if cache_version < DISKCACHE_VERSION_MULTIPLE_EXTENSIONS:
        # compare only the GWF content
        assert list(cacheman.cache.keys()) == ["gwf"]
        assert cacheman.cache["gwf"] == CACHE["gwf"]
    else:
        # compare everything
        assert cacheman.cache == CACHE


def test_parse_diskcache_error(app, tmp_path):
    cache_file = tmp_path / "cache.dat"
    cache_file.write_text("# version: 0x9999")
    cacheman = cache.CacheManager(app, cache_file)
    with pytest.raises(
        TypeError,
        match="cannot parse diskcache files with version '0x9999'",
    ):
        cacheman.parse()
