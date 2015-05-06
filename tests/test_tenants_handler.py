from agar.test import BaseTest, WebTest
from models import Tenant
from routes import application


class TestTenantsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestTenantsHandler, self).setUp()

    def tearDown(self):
        pass

    def testGet_ReturnsOKStatus(self):
        request_parameters = {}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def testPost_ReturnsCreatedStatus(self):
        request_parameters = {'tenant': {'name': 'ABC Flooring, Inc.'}}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.post_json(uri, params=request_parameters)
        self.assertEqual(201, response.status_code)

    def testPost_CreateNewTenant(self):
        request_parameters = {'tenant': {'name': 'ABC Flooring, Inc.'}}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.post_json(uri, params=request_parameters)
        actual = Tenant.find_by_name(request_parameters['tenant']['name'])
        self.assertIsNotNone(actual)

    def testPost_CreateNewTenant_SetsLocationHeader(self):
        request_parameters = {'tenant': {'name': 'ABC Flooring, Inc.'}}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.post_json(uri, params=request_parameters)
        actual = Tenant.find_by_name(request_parameters['tenant']['name'])
        tenant_uri = application.router.build(None,
                                              'tenants-mutator',
                                              None,
                                              {'tenant_id': actual.key.urlsafe()})
        self.assertTrue(tenant_uri in response.headers.get('Location'))

    def testPut_ReturnsNoContentStatus(self):
        uri = application.router.build(None, 'tenants-mutator', None, {'tenant_id': 'd836248623876'})
        response = self.app.put_json(uri)
        self.assertEqual(204, response.status_code)

    def testDelete_ReturnsNoContentStatus(self):
        uri = application.router.build(None, 'tenants-mutator', None, {'tenant_id': 'd836248623876'})
        response = self.app.delete(uri)
        self.assertEqual(204, response.status_code)
