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
      spyOn(RestangularProvider, 'addRequestInterceptor').and.callThrough()
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

    it 'should resolve \'domain\' state', ->
      expect($state.href('domain', {})).toEqual('#/domain')

    it 'should resolve \'deviceEdit\' state', ->
      expect($state.href('deviceEdit', {})).toEqual('#/deviceEdit')

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

    it 'should resolve \'apiTest\' state', ->
      expect($state.href('apiTest', {})).toEqual('#/api_testing')

    it 'should resolve \'remote_control\' state', ->
      expect($state.href('remote_control', {})).toEqual('#/remote_control')

  describe 'Restangular configuration', ->
    it 'sets the base URL', ->
      expect(RestangularProvider.setBaseUrl).toHaveBeenCalledWith '/api/v1'

    it 'sets the default headers', ->
      headers = {
        'Content-Type': 'application/json'
        'Accept': 'application/json'
        'Authorization': '6C346588BD4C6D722A1165B43C51C'
      }
      expect(RestangularProvider.setDefaultHeaders).toHaveBeenCalledWith headers

    it 'adds a request interceptor', ->
      expect(RestangularProvider.addRequestInterceptor).toHaveBeenCalled()
      args = RestangularProvider.addRequestInterceptor.calls.argsFor(0)
      expect(args[0] instanceof Function).toBeTruthy()

    it 'sets the Restangular fields mapping', ->
      restangularFieldsMapping = {id: 'key'}
      expect(RestangularProvider.setRestangularFields).toHaveBeenCalledWith restangularFieldsMapping
