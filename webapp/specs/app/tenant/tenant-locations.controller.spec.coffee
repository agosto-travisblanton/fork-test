'use strict'

describe 'TenantLocationsCtrl', ->
  scope = undefined
  $controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  LocationsService = undefined
  serviceInjection = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _TenantsService_, _LocationsService_, _$state_, _$rootScope_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    $rootScope = _$rootScope_
    TenantsService = _TenantsService_
    LocationsService = _LocationsService_
    scope = $rootScope.$new()
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      TenantsService: TenantsService
      LocationsService: LocationsService
    }

  describe '.initialize', ->
    tenantKey = 'some key'
    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      locationsServicePromise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue tenantsServicePromise
      spyOn(LocationsService, 'getLocationsByTenantKey').and.returnValue locationsServicePromise
      controller = $controller 'TenantLocationsCtrl', serviceInjection
      controller.tenantKey = tenantKey
      controller.initialize()

      it 'calls TenantsService.getTenantByKey with tenantKey', ->
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith tenantKey

      it 'calls LocationsService.getLocationsByTenantKey with tenantKey', ->
        expect(LocationsService.getLocationsByTenantKey).toHaveBeenCalledWith tenantKey

  describe '.editItem', ->
    item = {key: 'dhjad897d987fadafg708hb55'}
    beforeEach ->
      spyOn $state, 'go'
      controller = $controller 'TenantLocationsCtrl', serviceInjection
      controller.editItem item

    it "routes to the 'editLocation' named route, passing the supplied location key", ->
      expect($state.go).toHaveBeenCalledWith 'editLocation', {locationKey: item.key}


