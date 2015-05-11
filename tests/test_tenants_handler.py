import json
from pprint import pprint
from agar.test import BaseTest, WebTest
from models import Tenant, TenantEntityGroup
from routes import application


class TestTenantsHandler(BaseTest, WebTest):
    APPLICATION = application

    def setUp(self):
        super(TestTenantsHandler, self).setUp()

    def testGetById_ReturnsOKStatus(self):
        tenant_keys = self.loadTenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenant-accessor', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def testGetById_ReturnsTenantRepresentation(self):
        tenant_keys = self.loadTenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenant-accessor', None, {'tenant_key': tenant_keys[0].urlsafe()})
        response = self.app.get(uri, params=request_parameters)
        response_json = json.loads(response.body)
        # pprint(response_json)
        expected = tenant_keys[0].get()
        self.assertEqual(response_json.get('key'), expected.key.urlsafe())
        self.assertEqual(response_json.get('name'), expected.name)
        self.assertEqual(response_json.get('created'), expected.created.strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual(response_json.get('updated'), expected.updated.strftime('%Y-%m-%d %H:%M:%S'))

    def testGet_ReturnsOKStatus(self):
        self.loadTenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.get(uri, params=request_parameters)
        self.assertOK(response)

    def testGet_ReturnsJsonResources(self):
        self.loadTenants()
        request_parameters = {}
        uri = application.router.build(None, 'tenants', None, {})
        response = self.app.get(uri, params=request_parameters)
        response_json = json.loads(response.body)
        # pprint(response_json)
        self.assertEqual(len(response_json), 5)

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
                                              'tenant-mutator',
                                              None,
                                              {'tenant_id': actual.key.urlsafe()})
        self.assertTrue(tenant_uri in response.headers.get('Location'))

    def testPut_ReturnsNoContentStatus(self):
        uri = application.router.build(None, 'tenant-mutator', None, {'tenant_id': 'd836248623876'})
        response = self.app.put_json(uri)
        self.assertEqual(204, response.status_code)

    def testDelete_ReturnsNoContentStatus(self):
        uri = application.router.build(None, 'tenant-mutator', None, {'tenant_id': 'd836248623876'})
        response = self.app.delete(uri)
        self.assertEqual(204, response.status_code)

    def loadTenants(self):
        tenant_keys = []
        for x in range(5):
            tenant_entity_group = TenantEntityGroup.singleton()
            tenant = Tenant(parent=tenant_entity_group.key,
                            name="Testing tenant {0}".format(x))
            tenant_key = tenant.put()
            tenant_keys.append(tenant_key)
        return tenant_keys