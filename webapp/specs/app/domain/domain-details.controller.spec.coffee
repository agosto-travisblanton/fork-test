'use strict'

describe 'DomainDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DomainsService = undefined
  domainsServicePromise = undefined
  domain = {
    key: 'ahjad897d987fadafg708fg71',
    name: 'bob.agosto.com',
    impersonation_admin_email_address: 'bob.macneal@skykit.com',
    created: '2015-09-08 12:15:08',
    updated: '2015-09-08 12:15:08'
  }

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DomainsService_) ->
    $controller = _$controller_
    $stateParams = {}
    $state = {}
    DomainsService = _DomainsService_

  describe 'initialization', ->
    beforeEach ->
      domainsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DomainsService, 'getDomainByKey').and.returnValue domainsServicePromise

    describe 'new mode', ->
      beforeEach ->
        controller = $controller 'DomainDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DomainsService: DomainsService
        }

      it 'currentDomain property should be defined', ->
        expect(controller.currentDomain).toBeDefined()

    describe 'edit mode', ->
      beforeEach ->
        $stateParams.domainKey = 'fkasdhfjfa9s8udyva7dygoudyg'
        controller = $controller 'DomainDetailsCtrl', {
          $stateParams: $stateParams
          $state: $state
          DomainsService: DomainsService
        }

      it 'currentDomain property should be defined', ->
        expect(controller.currentDomain).toBeDefined()

      it 'call DomainsService.getDomainByKey to retrieve the selected domain', ->
        expect(DomainsService.getDomainByKey).toHaveBeenCalledWith($stateParams.domainKey)

      it "the 'then' handler caches the retrieved domain in the controller", ->
        domainsServicePromise.resolve domain
        expect(controller.currentDomain).toBe domain

