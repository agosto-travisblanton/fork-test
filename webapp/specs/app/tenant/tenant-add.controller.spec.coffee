'use strict'

describe 'TenantAddCtrl', ->
  $cookies = undefined
  controllerFactory = undefined
  controller = undefined
  controllerGameStop = undefined
  DistributorsService = undefined
  distributorKey = 'ahtzfnNreWtpdC1kaXNwbGF5LWRldml0aXR5R3JvdXAMCxILRGlzdHJpYnV0b3IYgICAgMCcggoM'
  distributorPromise = undefined
  distributorDomainsPromise = undefined
  TenantsService = undefined
  tenantsServicePromise = undefined
  progressBarService = undefined
  $state = undefined
  sweet = undefined
  $log = undefined
  $location = undefined

  beforeEach ->
    angular.mock.module 'skykitProvisioning'

    inject (_$controller_, _$cookies_, _DistributorsService_, _TenantsService_, _$state_, _sweet_, _$log_, _$location_) ->
      controllerFactory = _$controller_
      $cookies = _$cookies_
      DistributorsService = _DistributorsService_
      TenantsService = _TenantsService_
      $state = _$state_
      sweet = _sweet_
      $log = _$log_
      $location = _$location_
      progressBarService = {
        start: ->
        complete: ->
      }
      controller = controllerFactory('TenantAddCtrl',
        {
          $cookies: $cookies,
          DistributorsService: DistributorsService,
          TenantsService: TenantsService,
          ProgressBarService: progressBarService,
          $location: {
            host: () ->
              return 'localhost'
          }
        }
      )
      controllerGameStop = controllerFactory('TenantAddCtrl',
        {
          $location: {
            host: () ->
              return 'provisioning-gamestop'
          }
        }
      )
      return

  describe 'upon instantiation', ->
    it 'sets gameStopServer false unless on GameStop host', ->
      expect(controller.gameStopServer).toBeFalsy()
      expect(controllerGameStop.gameStopServer).toBeTruthy()

    it 'declares a currentTenant who is active and has proof of play turned off', ->
      expect(controller.currentTenant).toBeDefined()
      expect(controller.currentTenant.active).toBeTruthy()
      expect(controller.currentTenant.proof_of_play_logging).toBeFalsy()

    it 'declares a currentTenant that has content_manager_url declared but not defined', ->
      expect(controller.currentTenant.content_manager_url).toBeUndefined()

    it 'declares a currentTenant that has player_content_url declared but not defined', ->
      expect(controller.currentTenant.player_content_url).toBeUndefined()

    it 'declares a selectedDomain', ->
      expect(controller.selectedDomain).toBeUndefined()

    it 'declares distributorDomains as an empty array', ->
      expect(angular.isArray(controller.distributorDomains)).toBeTruthy()
      expect(controller.distributorDomains.length).toBe 0

  describe '.initialize', ->
    beforeEach ->
      spyOn($cookies, 'get').and.returnValue distributorKey
      distributorPromise = new skykitProvisioning.q.Mock
      spyOn(DistributorsService, 'getByKey').and.returnValue distributorPromise
      distributorDomainsPromise = new skykitProvisioning.q.Mock
      spyOn(DistributorsService, 'getDomainsByKey').and.returnValue distributorDomainsPromise
      controller.initialize()

    it 'invokes $cookies to obtain the currentDistributorKey', ->
      expect($cookies.get).toHaveBeenCalledWith 'currentDistributorKey'

    it 'sets the currentDistributorKey from $cookies', ->
      expect(controller.currentDistributorKey).toBe distributorKey

    it 'calls DistributorsService with distributorKey to get the distributor', ->
      expect(DistributorsService.getByKey).toHaveBeenCalledWith distributorKey

    it 'calls DistributorsService with distributorKey to get the distributor domains', ->
      expect(DistributorsService.getDomainsByKey).toHaveBeenCalledWith distributorKey

  describe '.onClickSaveButton', ->
    domain_key = undefined

    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      spyOn(TenantsService, 'save').and.returnValue tenantsServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      spyOn(sweet, 'show')
      domain_key = 'ahf39fnNreWtpdC1kaXNwbGF5LWRlxXml0aXR8R3UvdXAMCxILRGlzdHJpYnV0b3IYgICAgMCc09oM'
      controller.selectedDomain = {key: domain_key}
      controller.onClickSaveButton()

    it 'sets the domain_key on the current tenant from the selected domain', ->
      expect(controller.currentTenant.domain_key).toEqual domain_key

    it 'starts the progress bar animation', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'calls TenantsService.save with the current tenant', ->
      expect(TenantsService.save).toHaveBeenCalledWith controller.currentTenant

    describe '.onSuccessTenantSave', ->
      beforeEach ->
        spyOn($state, 'go')
        controller.onSuccessTenantSave()

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation back to 'tenants'", ->
        expect($state.go).toHaveBeenCalledWith 'tenants'

    describe '.onFailureTenantSave 409 conflict', ->
      beforeEach ->
        errorObject = {status: 409}
        controller.onFailureTenantSave errorObject

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "show the error dialog", ->
        expectedError = 'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

    describe '.onFailureTenantSave general error', ->
      errorObject = undefined

      beforeEach ->
        spyOn($log, 'error')
        errorObject = {status: 400}
        controller.onFailureTenantSave errorObject

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'logs the error', ->
        expect($log.error).toHaveBeenCalledWith errorObject

      it "show the error dialog", ->
        expectedError = 'Unable to save the tenant.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

  describe '.autoGenerateTenantCode', ->
    it 'generates a new tenant code when key is undefined', ->
      controller.currentTenant.key = undefined
      controller.currentTenant.name = 'Foobar Inc.'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'foobar_inc'

    it 'skips generating a new tenant code when key is defined', ->
      controller.currentTenant.key = 'd8ad97ad87afg897f987g0f8'
      controller.currentTenant.name = 'Foobar Inc.'
      controller.currentTenant.tenant_code = 'foobar_inc'
      controller.autoGenerateTenantCode()
      expect(controller.currentTenant.tenant_code).toBe 'foobar_inc'
