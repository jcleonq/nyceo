# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import nyc.eo


class NycEoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=nyc.eo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'nyc.eo:default')


NYC_EO_FIXTURE = NycEoLayer()


NYC_EO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NYC_EO_FIXTURE,),
    name='NycEoLayer:IntegrationTesting',
)


NYC_EO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(NYC_EO_FIXTURE,),
    name='NycEoLayer:FunctionalTesting',
)


NYC_EO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        NYC_EO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='NycEoLayer:AcceptanceTesting',
)
