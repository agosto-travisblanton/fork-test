'use strict'

describe 'DomainDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DomainsService = undefined
  domainsServicePromise = undefined
  DistributorsService = undefined
  distributorsServicePromise = undefined
  progressBarService = undefined
  sweet = undefined
  serviceInjection = undefined

  domain = {
    key: 'ahjad897d987fadafg708fg71',
    name: 'bob.agosto.com',
    impersonation_admin_email_address: 'bob.macneal@skykit.com',
    created: '2015-09-08 12:15:08',
    updated: '2015-09-08 12:15:08'
  }

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _DomainsService_, _DistributorsService_, _sweet_) ->
    $controller = _$controller_
    $stateParams = {}
    $state = {}
    DomainsService = _DomainsService_
    DistributorsService = _DistributorsService_
    progressBarService = {
      start: ->
      complete: ->
    }
    sweet = _sweet_
    scope = {}
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      ProgressBarService: progressBarService
      DomainsService: DomainsService
      DistributorsService: DistributorsService
    }

  describe 'initialization', ->
    beforeEach ->
      domainsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      distributorsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DomainsService, 'getDomainByKey').and.returnValue domainsServicePromise
      spyOn(DistributorsService, 'getByName').and.returnValue distributorsServicePromise

    describe 'new mode', ->
      beforeEach ->
        controller = $controller 'DomainDetailsCtrl', serviceInjection

      it 'currentDomain property should be defined', ->
        expect(controller.currentDomain).toBeDefined()

      it 'defaultDistributor property should be Agosto', ->
        expect(controller.defaultDistributor).toEqual 'Agosto'

    describe '.initialize', ->
      beforeEach ->
        controller = $controller 'DomainDetailsCtrl', serviceInjection

      it 'calls DistributorsService.getByName to retrieve default distributor', ->
        controller.initialize()
        expect(DistributorsService.getByName).toHaveBeenCalledWith(controller.defaultDistributor)

    describe 'edit mode', ->
      beforeEach ->
        $stateParams.domainKey = 'fkasdhfjfa9s8udyva7dygoudyg'
        controller = $controller 'DomainDetailsCtrl', serviceInjection

      it 'currentDomain property should be defined', ->
        expect(controller.currentDomain).toBeDefined()

      it 'call DomainsService.getDomainByKey to retrieve the selected domain', ->
        expect(DomainsService.getDomainByKey).toHaveBeenCalledWith($stateParams.domainKey)

      it "the 'then' handler caches the retrieved domain in the controller", ->
        domainsServicePromise.resolve domain
        expect(controller.currentDomain).toBe domain

  describe '.onClickSaveButton', ->
    beforeEach ->
      domainsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DomainsService, 'save').and.returnValue domainsServicePromise
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'DomainDetailsCtrl', serviceInjection

    it 'start the progress bar animation', ->
      controller.onClickSaveButton()
      domainsServicePromise.resolve()
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DomainsService.save, pass the current domain', ->
      controller.onClickSaveButton()
      domainsServicePromise.resolve()
      expect(DomainsService.save).toHaveBeenCalledWith(controller.currentDomain)
