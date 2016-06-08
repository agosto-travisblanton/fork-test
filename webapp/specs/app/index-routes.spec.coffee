'use strict'

describe 'skykitProvisioning module and configuration', ->
  $rootScope = undefined
  $state = undefined
  SessionsService = undefined
  $q = undefined
  $injector = undefined
  AuthorizationService = undefined
  RestangularProvider = undefined

  beforeEach ->
    module "restangular", (_RestangularProvider_, _$q_, _SessionsService_) ->
      RestangularProvider = _RestangularProvider_
      $q = _$q_
      SessionsService = _SessionsService_

      spyOn(RestangularProvider, 'setBaseUrl').and.callThrough()
      spyOn(RestangularProvider, 'addRequestInterceptor').and.callThrough()
      spyOn(RestangularProvider, 'addResponseInterceptor').and.callThrough()
      spyOn(RestangularProvider, 'setRestangularFields').and.callThrough()

    module 'skykitProvisioning'

    inject (_$rootScope_, _$state_, _$injector_, $templateCache, _$q_, _SessionsService_, _AuthorizationService_) ->
      RestangularProvider = _RestangularProvider_
      $q = _$q_
      SessionsService = _SessionsService_
      AuthorizationService = _AuthorizationService_
      $rootScope = _$rootScope_
      $state = _$state_
      $injector = _$injector_
      # We need add the template entry into the templateCache if we ever specify a templateUrl
      $templateCache.put 'template.html', ''

  
    describe 'URL resolution', ->
      it 'should resolve \'home\' state', ->
        expect($state.href('home', {})).toEqual('#/')
  
      it 'should resolve \'proof\' state', ->
        expect($state.href('proof', {})).toEqual('#/proof')
  
      it 'should resolve \'domains\' state', ->
        expect($state.href('domains', {})).toEqual('#/domains')
  
      it 'should resolve \'addDomain\' state', ->
        expect($state.href('addDomain', {})).toEqual('#/domains/add')
  
      it 'should resolve \'editDomain\' state', ->
        domainKey = 'deree0re9reuewqerer'
        expect($state.href('editDomain', {domainKey: domainKey})).toEqual("#/domains/#{domainKey}")
  
      it 'should resolve \'devices\' state', ->
        expect($state.href('devices', {})).toEqual('#/devices')
  
      it 'should resolve \'tenants\' state', ->
        expect($state.href('tenants', {})).toEqual('#/tenants')
  
      it 'should resolve \'addTenant\' state', ->
        expect($state.href('addTenant', {})).toEqual('#/tenants/add')
  
      it 'should resolve \'tenantDetails\' state', ->
        tenantKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6'
        expect($state.href('tenantDetails', {tenantKey: tenantKey})).toEqual("#/tenants/#{tenantKey}/details")
  
      it 'should resolve \'editDevice\' state', ->
        deviceKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6'
        expect($state.href('editDevice', {deviceKey: deviceKey})).toEqual("#/devices/#{deviceKey}")
  
    describe 'breadcrumbs', ->
      describe 'labels', ->
        it 'should resolve \'home\' state', ->
          expect($state.get('home').ncyBreadcrumb.label).toBe 'Skykit Provisioning'
  
        it 'should resolve \'welcome\' state', ->
          expect($state.get('welcome').ncyBreadcrumb.label).toBe 'Skykit Provisioning'
  
        it 'should resolve \'domains\' state', ->
          expect($state.get('domains').ncyBreadcrumb.label).toBe 'Domains'
  
        it 'should resolve \'addDomain\' state', ->
          expect($state.get('addDomain').ncyBreadcrumb.label).toBe 'Add domain'
  
        it 'should resolve \'editDomain\' state', ->
          expect($state.get('editDomain').ncyBreadcrumb.label).toBe '{{ domainDetailsCtrl.currentDomain.name }}'
  
        it 'should resolve \'tenants\' state', ->
          expect($state.get('tenants').ncyBreadcrumb.label).toBe 'Tenants'
  
        it 'should resolve \'addTenant\' state', ->
          expect($state.get('addTenant').ncyBreadcrumb.label).toBe 'Add tenant'
  
        it 'should resolve \'tenantDetails\' state', ->
          expect($state.get('tenantDetails').ncyBreadcrumb.label).toBe '{{ tenantDetailsCtrl.currentTenant.name }}'
  
        it 'should resolve \'tenantManagedDevices\' state', ->
          expect($state.get('tenantManagedDevices').ncyBreadcrumb.label).toBe
          '{{ tenantManagedDevicesCtrl.currentTenant.name }}'
  
        it 'should resolve \'tenantUnmanagedDevices\' state', ->
          expect($state.get('tenantUnmanagedDevices').ncyBreadcrumb.label).toBe
          '{{ tenantUnmanagedDevicesCtrl.currentTenant.name }}'
  
        it 'should resolve \'tenantLocations\' state', ->
          expect($state.get('tenantLocations').ncyBreadcrumb.label).toBe '{{ tenantLocationsCtrl.currentTenant.name }}'
  
        it 'should resolve \'addLocation\' state', ->
          expect($state.get('addLocation').ncyBreadcrumb.label).toBe '{{ tenantLocationCtrl.tenantName }}  / Location'
  
        it 'should resolve \'editLocation\' state', ->
          expect($state.get('editLocation').ncyBreadcrumb.label).toBe
          '{{ tenantLocationCtrl.tenantName }}  / {{ tenantLocationCtrl.locationName }}'
  
        it 'should resolve \'devices\' state', ->
          expect($state.get('devices').ncyBreadcrumb.label).toBe 'Devices'
  
        it 'should resolve \'editDevice\' state', ->
          expect($state.get('editDevice').ncyBreadcrumb.label).toBe '{{ deviceDetailsCtrl.currentDevice.key }}'
  
        it 'should resolve \'proof\' state', ->
          expect($state.get('proof').ncyBreadcrumb.label).toBe 'Proof of Play'
  
      describe 'parents', ->
        it 'should resolve \'addTenant\' state', ->
          expect($state.get('addTenant').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'tenantDetails\' state', ->
          expect($state.get('tenantDetails').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'tenantManagedDevices\' state', ->
          expect($state.get('tenantManagedDevices').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'tenantUnmanagedDevices\' state', ->
          expect($state.get('tenantUnmanagedDevices').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'tenantLocations\' state', ->
          expect($state.get('tenantLocations').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'editLocation\' state', ->
          expect($state.get('editLocation').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'editDevice\' state', ->
          expect($state.get('editDevice').ncyBreadcrumb.parent).toBe 'devices'
  
        it 'should resolve \'addLocation\' state', ->
          expect($state.get('addLocation').ncyBreadcrumb.parent).toBe 'tenants'
  
        it 'should resolve \'addDomain\' state', ->
          expect($state.get('addDomain').ncyBreadcrumb.parent).toBe 'domains'
  
        it 'should resolve \'editDomain\' state', ->
          expect($state.get('editDomain').ncyBreadcrumb.parent).toBe 'domains'
  
  
  
    describe 'Restangular configuration', ->
      it 'sets the base URL', ->
        expect(RestangularProvider.setBaseUrl).toHaveBeenCalledWith '/api/v1'
  
      it 'adds a response interceptor', ->
        expect(RestangularProvider.addResponseInterceptor).toHaveBeenCalled()
        args = RestangularProvider.addResponseInterceptor.calls.argsFor(0)
        expect(args[0] instanceof Function).toBeTruthy()
  
      it 'sets the Restangular fields mapping', ->
        restangularFieldsMapping = {id: 'key'}
        expect(RestangularProvider.setRestangularFields).toHaveBeenCalledWith restangularFieldsMapping
  
