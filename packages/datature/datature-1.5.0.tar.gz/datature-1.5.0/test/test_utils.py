#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   test_utils.py
@Author  :   Raighne.Weng
@Version :   1.3.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Utils Test Cases
'''

import unittest
from test.fixture.data import decamelize_fixture
from datature.utils import utils


class TestUtils(unittest.TestCase):
    """Datature Utils Test Cases."""

    def test_selective_decamelize(self):
        """Test selective_decamelize function."""
        project_response = utils.selective_decamelize(
            decamelize_fixture.project_response)
        assert project_response == decamelize_fixture.decamelized_project_response

        quota_response = utils.selective_decamelize(
            decamelize_fixture.quota_response)

        assert quota_response == decamelize_fixture.decamelized_quota_response

        asset_response = utils.selective_decamelize(
            decamelize_fixture.asset_response)

        assert asset_response == decamelize_fixture.decamelized_asset_response

        artifact_response = utils.selective_decamelize(
            decamelize_fixture.artifact_response)
        assert artifact_response == decamelize_fixture.decamelized_artifact_response
