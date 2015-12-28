'use strict'

describe 'TenantDetailsCtrl', ->
  scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  $log = undefined
  TenantsService = undefined
  DomainsService = undefined
  DevicesService = undefined
  DistributorsService = undefined
  progressBarService = undefined
  tenantsServicePromise = undefined
  devicesServicePromise = undefined
  distributorsServicePromise = undefined
  distributorsDomainsServicePromise = undefined
  domainsServicePromise = undefined
  sweet = undefined
  serviceInjection = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _TenantsService_, _DomainsService_, _DevicesService_, _DistributorsService_,
    _$state_, _sweet_, _$log_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    TenantsService = _TenantsService_
    DomainsService = _DomainsService_
    DevicesService = _DevicesService_
    DistributorsService = _DistributorsService_
    progressBarService = {
      start: ->
      complete: ->
    }
    sweet = _sweet_
    $log = _$log_
    scope = {}
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      ProgressBarService: progressBarService
    }

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      distributorsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      distributorsDomainsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      domainsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise)
      spyOn(DevicesService, 'getDevicesByTenant').and.returnValue(devicesServicePromise)
      spyOn(DistributorsService, 'getDomainsByKey').and.returnValue(distributorsDomainsServicePromise)
      spyOn(DomainsService, 'getDomainByKey').and.returnValue(domainsServicePromise)

    it 'currentTenant should be set', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.currentTenant).toBeDefined()
      expect(controller.currentTenant.key).toBeUndefined()
      expect(controller.currentTenant.name).toBeUndefined()
      expect(controller.currentTenant.tenant_code).toBeUndefined()
      expect(controller.currentTenant.admin_email).toBeUndefined()
      expect(controller.currentTenant.content_server_url).toBeUndefined()
      expect(controller.currentTenant.chrome_device_domain).toBeUndefined()
      expect(controller.currentTenant.domain_key).toBeUndefined()
      expect(controller.currentTenant.notification_emails).toBeUndefined()
      expect(controller.currentTenant.active).toBeTruthy()

    it 'selectedDomain should be defined', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.selectedDomain).toBeUndefined()

    it 'currentTenantDisplays property should be defined', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.currentTenantDisplays).toBeDefined()

    it 'distributorDomains property should be defined', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.distributorDomains).toBeDefined()

    describe 'editing an existing tenant', ->
      beforeEach ->
        $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
        serviceInjection = {
          $scope: scope
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

      it 'retrieve tenant\'s devices by tenant key from DevicesService', ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        devices = [{key: 'f8sa76d78fa978d6fa7dg7ds55'}, {key: 'f8sa76d78fa978d6fa7dg7ds56'}]
        data = {objects: devices}
        devicesServicePromise.resolve(data)
        expect(DevicesService.getDevicesByTenant).toHaveBeenCalledWith($stateParams.tenantKey)
        expect(controller.currentTenantDisplays).toBe(devices)

    describe 'creating a new tenant', ->
      it 'editMode should be set to false', ->
        $stateParams = {}
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        expect(controller.editMode).toBeFalsy()

      it 'do not call TenantsService.getTenantByKey', ->
        $stateParams = {}
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        expect(TenantsService.getTenantByKey).not.toHaveBeenCalled()

      it 'do not call Devices.getDevicesByTenant', ->
        $stateParams = {}
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        expect(DevicesService.getDevicesByTenant).not.toHaveBeenCalled()

    describe '.initialize', ->
      beforeEach ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection
        controller.currentDistributorKey = 'some-key'

      it 'calls DistributorsService.getDomainsByKey to retrieve distributor domains', ->
        controller.initialize()
        expect(DistributorsService.getDomainsByKey).toHaveBeenCalledWith controller.currentDistributorKey

  describe '.onClickSaveButton', ->
    domain_key = undefined

    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'save').and.returnValue(tenantsServicePromise)
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
      expect(TenantsService.save).toHaveBeenCalledWith(controller.currentTenant)

    describe '.onSuccessTenantSave', ->
      beforeEach ->
        controller.onSuccessTenantSave()

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation back to 'tenants'", ->
        expect($state.go).toHaveBeenCalledWith('tenants')

    describe '.onFailureTenantSave 409 conflict', ->
      beforeEach ->
        spyOn(sweet, 'show')
        errorObject = {status: 409}
        controller.onFailureTenantSave(errorObject)

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation back to 'tenants'", ->
        expect($state.go).toHaveBeenCalledWith('tenants')

      it "show the error dialog", ->
        expectedError = 'Tenant code unavailable. Please try a different tenant code.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

    describe '.onFailureTenantSave general error', ->
      beforeEach ->
        spyOn(sweet, 'show')
        spyOn($log, 'error')
        @errorObject = {status: 400}
        controller.onFailureTenantSave(@errorObject)

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "the 'then' handler routes navigation back to 'tenants'", ->
        expect($state.go).toHaveBeenCalledWith('tenants')

      it "show the error dialog", ->
        expectedError = 'Unable to save the tenant.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

      it "logs the error to the console", ->
        expect($log.error).toHaveBeenCalledWith @errorObject

  describe '.autoGenerateTenantCode', ->
    beforeEach ->
      $stateParams = {}
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
