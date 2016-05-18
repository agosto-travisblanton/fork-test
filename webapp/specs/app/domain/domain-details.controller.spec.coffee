'use strict'

describe 'DomainDetailsCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  $log = undefined
  DomainsService = undefined
  ToastsService = undefined
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

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _DomainsService_, _DistributorsService_, _sweet_, _ToastsService_, _$log_) ->
    $controller = _$controller_
    $stateParams = {}
    $state = {}
    $log = _$log_
    DomainsService = _DomainsService_
    DistributorsService = _DistributorsService_
    progressBarService = {
      start: ->
      complete: ->
    }
    sweet = _sweet_
    ToastsService = _ToastsService_
    scope = {}
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      ProgressBarService: progressBarService
      DomainsService: DomainsService
      DistributorsService: DistributorsService
      ToastsService: ToastsService
    }

  describe 'initialization', ->
    beforeEach ->
      domainsServicePromise = new skykitProvisioning.q.Mock
      distributorsServicePromise = new skykitProvisioning.q.Mock
      spyOn(DomainsService, 'getDomainByKey').and.returnValue domainsServicePromise
      spyOn(DistributorsService, 'getByName').and.returnValue distributorsServicePromise

    describe 'new mode', ->
      beforeEach ->
        controller = $controller 'DomainDetailsCtrl', serviceInjection

      it 'currentDomain property should be defined', ->
        expect(controller.currentDomain).toBeDefined()

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

  describe '.onSaveDomain', ->
    beforeEach ->
      domainsServicePromise = new skykitProvisioning.q.Mock
      spyOn(DomainsService, 'save').and.returnValue domainsServicePromise
      spyOn(progressBarService, 'start')
      controller = $controller 'DomainDetailsCtrl', serviceInjection
      controller.onSaveDomain()

    it 'starts the progress bar', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call DevicesService.save with the current device', ->
      expect(DomainsService.save).toHaveBeenCalledWith controller.currentDomain

    describe '.onSuccessSaveDomain', ->
      beforeEach ->
        spyOn(progressBarService, 'complete')
        spyOn(ToastsService, 'showSuccessToast')
        controller.onSuccessSaveDomain()

      it 'stops the progress bar', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "displays a success toast", ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith 'We saved your update.'

    describe '.onFailureSaveDomain', ->
      errorObject = {status: 409, statusText: 'Conflict'}

      beforeEach ->
        spyOn(progressBarService, 'complete')

      it 'stops the progress bar', ->
        controller.onFailureSaveDomain errorObject
        expect(progressBarService.complete).toHaveBeenCalled()

      describe '409 conflict returned from server', ->
        beforeEach ->
          spyOn(sweet, 'show')
          spyOn($log, 'info')
          controller.onFailureSaveDomain errorObject

        it 'displays a sweet alert when domain conflicts with existing domain', ->
          expect(sweet.show).toHaveBeenCalledWith('Oops...',
            'This domain name already exist. Please enter a unique domain name.', 'error')

        it 'logs info to the console when domain conflicts with existing domain', ->
          infoMessage = "Failure saving domain. Domain already exists: #{errorObject.status} #{errorObject.statusText}"
          expect($log.info).toHaveBeenCalledWith infoMessage

      describe 'general error returned from server', ->
        generalError = {status: 400, statusText: 'Some error'}

        beforeEach ->
          spyOn($log, 'error')
          spyOn(ToastsService, 'showErrorToast')
          controller.onFailureSaveDomain generalError

        it 'logs error to the console', ->
          errorMessage = "Failure saving domain: #{generalError.status} #{generalError.statusText}"
          expect($log.error).toHaveBeenCalledWith errorMessage

        it 'displays a toast regarding failure to save the domain', ->
          toastMessage = 'Oops. We were unable to save your updates at this time.'
          expect(ToastsService.showErrorToast).toHaveBeenCalledWith toastMessage
