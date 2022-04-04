# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from nyc.eo.testing import NYC_EO_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that nyc.eo is properly installed."""

    layer = NYC_EO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if nyc.eo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'nyc.eo'))

    def test_browserlayer(self):
        """Test that INycEoLayer is registered."""
        from nyc.eo.interfaces import (
            INycEoLayer)
        from plone.browserlayer import utils
        self.assertIn(
            INycEoLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = NYC_EO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['nyc.eo'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if nyc.eo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'nyc.eo'))

    def test_browserlayer_removed(self):
        """Test that INycEoLayer is removed."""
        from nyc.eo.interfaces import \
            INycEoLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            INycEoLayer,
            utils.registered_layers())
