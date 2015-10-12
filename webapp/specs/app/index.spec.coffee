'use strict'

describe 'skykitDisplayDeviceManagement module and configuration', ->
  $rootScope = undefined
  $state = undefined
  $injector = undefined
  RestangularProvider = undefined

  beforeEach ->
    module "restangular", (_RestangularProvider_) ->
      RestangularProvider = _RestangularProvider_
      spyOn(RestangularProvider, 'setBaseUrl').and.callThrough()
      spyOn(RestangularProvider, 'setDefaultHeaders').and.callThrough()
#      spyOn(RestangularProvider, 'addRequestInterceptor').and.callThrough()
      spyOn(RestangularProvider, 'addResponseInterceptor').and.callThrough()
      spyOn(RestangularProvider, 'setRestangularFields').and.callThrough()

    module 'skykitDisplayDeviceManagement'

    inject (_$rootScope_, _$state_, _$injector_, $templateCache) ->
      $rootScope = _$rootScope_
      $state = _$state_
      $injector = _$injector_
      # We need add the template entry into the templateCache if we ever specify a templateUrl
      $templateCache.put 'template.html', ''


  describe 'URL resolution', ->
    it 'should resolve \'home\' state', ->
      expect($state.href('home', {})).toEqual('#/')

    it 'should resolve \'version\' state', ->
      expect($state.href('version', {})).toEqual('#/version')

    it 'should resolve \'domains\' state', ->
      expect($state.href('domains', {})).toEqual('#/domains')

    it 'should resolve \'newDomain\' state', ->
      expect($state.href('newDomain', {})).toEqual('#/domains/new')

    it 'should resolve \'editDomain\' state', ->
      domainKey = 'deree0re9reuewqerer'
      expect($state.href('editDomain', {domainKey: domainKey})).toEqual("#/domains/#{domainKey}")

    it 'should resolve \'devices\' state', ->
      expect($state.href('devices', {})).toEqual('#/devices')

    it 'should resolve \'tenants\' state', ->
      expect($state.href('tenants', {})).toEqual('#/tenants')

    it 'should resolve \'newTenant\' state', ->
      expect($state.href('newTenant', {})).toEqual('#/tenants/new')

    it 'should resolve \'editTenant\' state', ->
      tenantKey = '3741833e781236b4jwdfhhfds98fyasd6fa7d6'
      expect($state.href('editTenant', {tenantKey: tenantKey})).toEqual("#/tenants/#{tenantKey}")

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
        expect($state.get('home').ncyBreadcrumb.label).toBe 'Home page'

      it 'should resolve \'welcome\' state', ->
        expect($state.get('welcome').ncyBreadcrumb.label).toBe 'Home page'

      it 'should resolve \'domains\' state', ->
        expect($state.get('domains').ncyBreadcrumb.label).toBe 'Domains'

      it 'should resolve \'tenants\' state', ->
        expect($state.get('tenants').ncyBreadcrumb.label).toBe 'Tenants'

      it 'should resolve \'newTenant\' state', ->
        expect($state.get('newTenant').ncyBreadcrumb.label).toBe 'New tenant'

      it 'should resolve \'editTenant\' state', ->
        expect($state.get('editTenant').ncyBreadcrumb.label).toBe '{{ tenantDetailsCtrl.currentTenant.name }}'

      it 'should resolve \'devices\' state', ->
        expect($state.get('devices').ncyBreadcrumb.label).toBe 'Devices'

      it 'should resolve \'editDevice\' state', ->
        expect($state.get('editDevice').ncyBreadcrumb.label).toBe '{{ deviceDetailsCtrl.currentDevice.key }}'

    describe 'parents', ->
      it 'should resolve \'newTenant\' state', ->
        expect($state.get('newTenant').ncyBreadcrumb.parent).toBe 'tenants'

      it 'should resolve \'editTenant\' state', ->
        expect($state.get('editTenant').ncyBreadcrumb.parent).toBe 'tenants'


  describe 'Restangular configuration', ->
    it 'sets the base URL', ->
      expect(RestangularProvider.setBaseUrl).toHaveBeenCalledWith '/api/v1'

#    it 'sets the default headers', ->
#      headers = {
#        'Content-Type': 'application/json'
#        'Accept': 'application/json'
#        'Authorization': '6C346588BD4C6D722A1165B43C51C'
#        'X-Provisioning-User': ''
#      }
#      expect(RestangularProvider.setDefaultHeaders).toHaveBeenCalled()

    it 'adds a request interceptor', ->
      spyOn(RestangularProvider, 'addRequestInterceptor').and.callThrough()
      expect(RestangularProvider.addRequestInterceptor).toHaveBeenCalled()
      args = RestangularProvider.addRequestInterceptor.calls.argsFor(0)
      expect(args[0] instanceof Function).toBeTruthy()

    it 'adds a response interceptor', ->
      expect(RestangularProvider.addResponseInterceptor).toHaveBeenCalled()
      args = RestangularProvider.addResponseInterceptor.calls.argsFor(0)
      expect(args[0] instanceof Function).toBeTruthy()

    it 'sets the Restangular fields mapping', ->
      restangularFieldsMapping = {id: 'key'}
      expect(RestangularProvider.setRestangularFields).toHaveBeenCalledWith restangularFieldsMapping
