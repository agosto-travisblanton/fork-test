'use strict'

describe 'skykitProvisioning module and configuration', ->
  $rootScope = undefined
  $state = undefined
  $injector = undefined
  RestangularProvider = undefined

  beforeEach ->
    module "restangular", (_RestangularProvider_) ->
      RestangularProvider = _RestangularProvider_
      spyOn(RestangularProvider, 'setBaseUrl').and.callThrough()
      spyOn(RestangularProvider, 'addRequestInterceptor').and.callThrough()
      spyOn(RestangularProvider, 'addResponseInterceptor').and.callThrough()
      spyOn(RestangularProvider, 'setRestangularFields').and.callThrough()

    module 'skykitProvisioning'

    inject (_$rootScope_, _$state_, _$injector_, $templateCache) ->
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

    it 'should resolve \'deviceReset\' state', ->
      deviceKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6'
      expect($state.href('deviceReset', {deviceKey: deviceKey})).toEqual("#/devices/#{deviceKey}/commands/reset")

    it 'should resolve \'deviceVolume\' state', ->
      deviceKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6'
      expect($state.href('deviceVolume', {deviceKey: deviceKey})).toEqual("#/devices/#{deviceKey}/commands/volume")

    it 'should resolve \'deviceCustom\' state', ->
      deviceKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6'
      expect($state.href('deviceCustom', {deviceKey: deviceKey})).toEqual("#/devices/#{deviceKey}/commands/custom")

  describe 'breadcrumbs', ->
    describe 'labels', ->
      it 'should resolve \'home\' state', ->
        expect($state.get('home').ncyBreadcrumb.label).toBe 'Skykit Provisioning'

      it 'should resolve \'welcome\' state', ->
        expect($state.get('welcome').ncyBreadcrumb.label).toBe 'Skykit Provisioning'

      it 'should resolve \'domains\' state', ->
        expect($state.get('domains').ncyBreadcrumb.label).toBe 'Domains'

      it 'should resolve \'tenants\' state', ->
        expect($state.get('tenants').ncyBreadcrumb.label).toBe 'Tenants'

      it 'should resolve \'addTenant\' state', ->
        expect($state.get('addTenant').ncyBreadcrumb.label).toBe 'Add tenant'

      it 'should resolve \'tenantDetails\' state', ->
        expect($state.get('tenantDetails').ncyBreadcrumb.label).toBe '{{ tenantDetailsCtrl.currentTenant.name }}'

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


  describe 'Restangular configuration', ->
    it 'sets the base URL', ->
      expect(RestangularProvider.setBaseUrl).toHaveBeenCalledWith '/api/v1'

#    it 'adds a request interceptor', ->
#      expect(RestangularProvider.addRequestInterceptor).toHaveBeenCalled()
#      args = RestangularProvider.addRequestInterceptor.calls.argsFor(0)
#      expect(args[0] instanceof Function).toBeTruthy()

    it 'adds a response interceptor', ->
      expect(RestangularProvider.addResponseInterceptor).toHaveBeenCalled()
      args = RestangularProvider.addResponseInterceptor.calls.argsFor(0)
      expect(args[0] instanceof Function).toBeTruthy()

    it 'sets the Restangular fields mapping', ->
      restangularFieldsMapping = {id: 'key'}
      expect(RestangularProvider.setRestangularFields).toHaveBeenCalledWith restangularFieldsMapping

