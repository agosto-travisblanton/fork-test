'use strict'

describe 'TenantDetailsCtrl', ->
  $scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  DomainsService = undefined
  TimezonesService = undefined
  DistributorsService = undefined
  progressBarService = undefined
  tenantsServicePromise = undefined
  distributorsServicePromise = undefined
  distributorsDomainsServicePromise = undefined
  domainsServicePromise = undefined
  timezoneServicePromise = undefined
  sweet = undefined
  serviceInjection = undefined

  beforeEach module('skykitProvisioning')
  beforeEach inject (_$controller_, _TenantsService_, _DomainsService_, _TimezonesService_, _DistributorsService_,
    _$state_, _sweet_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    TenantsService = _TenantsService_
    DomainsService = _DomainsService_
    TimezonesService = _TimezonesService_
    DistributorsService = _DistributorsService_
    progressBarService = {
      start: ->
      complete: ->
    }
    sweet = _sweet_
    $scope = {
      $watch: ->
    }
    serviceInjection = {
      $scope: $scope
      $stateParams: $stateParams
      ProgressBarService: progressBarService
    }

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      distributorsServicePromise = new skykitProvisioning.q.Mock
      distributorsDomainsServicePromise = new skykitProvisioning.q.Mock
      domainsServicePromise = new skykitProvisioning.q.Mock
      timezoneServicePromise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue tenantsServicePromise
      spyOn(DistributorsService, 'getDomainsByKey').and.returnValue distributorsDomainsServicePromise
      spyOn(DomainsService, 'getDomainByKey').and.returnValue domainsServicePromise
      spyOn(TimezonesService, 'getUsTimezones').and.returnValue timezoneServicePromise

    it 'gameStopServer should be set', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.gameStopServer).toBeDefined()

    it 'currentTenant should be set', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.currentTenant).toBeDefined()
      expect(controller.currentTenant.active).toBeTruthy()

    it 'selectedDomain should be defined', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.selectedDomain).toBeUndefined()

    it 'distributorDomains property should be defined', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.distributorDomains).toBeDefined()

    describe 'editing an existing tenant', ->
      beforeEach ->
        $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
        serviceInjection = {
          $scope: $scope
          $stateParams: $stateParams
          ProgressBarService: progressBarService
        }

      it 'editMode should be set to true', ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        expect(controller.editMode).toBeTruthy()

      it 'retrieve tenant by key from TenantsService', ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'}
        tenantsServicePromise.resolve(tenant)
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey)
        expect(controller.currentTenant).toBe(tenant)

    describe 'creating a new tenant', ->
      it 'editMode should be set to false', ->
        $stateParams = {}
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        expect(controller.editMode).toBeFalsy()

      it 'do not call TenantsService.getTenantByKey', ->
        $stateParams = {}
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        expect(TenantsService.getTenantByKey).not.toHaveBeenCalled()

    describe '.initialize', ->
      beforeEach ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        controller.currentDistributorKey = 'some-key'

      it 'calls TimezonesService.getUsTimezones to retrieve US timezones', ->
        controller.initialize()
        expect(TimezonesService.getUsTimezones).toHaveBeenCalled()

      it 'calls DistributorsService.getDomainsByKey to retrieve distributor domains', ->
        controller.initialize()
        expect(DistributorsService.getDomainsByKey).toHaveBeenCalledWith controller.currentDistributorKey

    describe '.onSuccessResolvingTenant', ->
      tenant = {domain_key: 'some_key'}
      beforeEach ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection

      it 'calls DomainsService.getDomainByKey to retrieve domain', ->
        controller.onSuccessResolvingTenant tenant
        expect(DomainsService.getDomainByKey).toHaveBeenCalledWith tenant.domain_key

  describe '.onClickSaveButton', ->
    domain_key = undefined

    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'save').and.returnValue tenantsServicePromise
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      domain_key = '1231231231312'
      controller.selectedDomain = {key: domain_key}
      controller.onClickSaveButton()
      tenantsServicePromise.resolve()

    it 'sets the domain_key on the current tenant from the selected domain', ->
      expect(controller.currentTenant.domain_key).toEqual domain_key

    it 'starts the progress bar animation', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call TenantsService.save, pass the current tenant', ->
      expect(TenantsService.save).toHaveBeenCalledWith controller.currentTenant

    describe '.onSuccessTenantSave', ->
      beforeEach ->
        controller.onSuccessTenantSave()

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()


    describe '.onFailureTenantSave 409 conflict', ->
      beforeEach ->
        spyOn(sweet, 'show')
        errorObject = {status: 409}
        controller.onFailureTenantSave errorObject

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()


      it "show the error dialog", ->
        expectedError = 'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

    describe '.onFailureTenantSave general error', ->
      beforeEach ->
        spyOn(sweet, 'show')
        @errorObject = {status: 400}
        controller.onFailureTenantSave(@errorObject)

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "show the error dialog", ->
        expectedError = 'Unable to save the tenant.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

  describe '.autoGenerateTenantCode', ->
    beforeEach ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection

    it 'generates a new tenant code when key is undefined', ->
      controller.currentTenant.key = undefined
      controller.currentTenant.name = 'Super Duper Foobar Inc.'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'super_duper_foobar_inc'

    it 'skips generating a new tenant code when key is defined', ->
      controller.currentTenant.key = 'd8ad97ad87afg897f987g0f8'
      controller.currentTenant.name = 'Foobar Inc.'
      controller.currentTenant.tenant_code = 'barfoo_company'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'barfoo_company'
