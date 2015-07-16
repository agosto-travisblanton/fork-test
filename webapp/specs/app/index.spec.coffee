'use strict'

describe 'skykitDisplayDeviceManagement module and configuration', ->
  $rootScope = undefined
  $state = undefined
  $injector = undefined

  beforeEach ->
    module 'skykitDisplayDeviceManagement'
    inject((_$rootScope_, _$state_, _$injector_, $templateCache) ->
      $rootScope = _$rootScope_
      $state = _$state_
      $injector = _$injector_
      # We need add the template entry into the templateCache if we ever specify a templateUrl
      $templateCache.put 'template.html', ''
    )

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

