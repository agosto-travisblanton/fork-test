'use strict'

describe 'DisplayDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DisplaysService = undefined
  displaysServicePromise = undefined
  TenantsService = undefined
  tenantsServicePromise = undefined
  displays = [
    {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]
  tenants = [
    {key: 'dhjad897d987fadafg708fg7d', name: 'Foobar1', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708y67d', name: 'Foobar2', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    {key: 'dhjad897d987fadafg708hb55', name: 'Foobar3', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
  ]


  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DisplaysService_, _TenantsService_, _$stateParams_, _$state_) ->
    $controller = _$controller_
    $stateParams = _$stateParams_
    $state = _$state_
    DisplaysService = _DisplaysService_
    TenantsService = _TenantsService_

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'fetchAllTenants').and.returnValue tenantsServicePromise
      displaysServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DisplaysService, 'getByKey').and.returnValue displaysServicePromise
      controller = $controller 'DisplayDetailsCtrl', {
        $stateParams: $stateParams
        $state: $state
        DisplaysService: DisplaysService
        TenantsService: TenantsService
      }

    it 'currentDisplay property should be defined', ->
      expect(controller.currentDisplay).toBeDefined()

    it 'call TenantsService.fetchAllTenants to retrieve all tenants', ->
      expect(TenantsService.fetchAllTenants).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved tenants in the controller", ->
      tenantsServicePromise.resolve tenants
      expect(controller.tenants).toBe tenants

