'use strict'

describe 'TenantDetailsCtrl', ->
  scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  DevicesService = undefined
  DistributorsService = undefined
  progressBarService = undefined
  tenantsServicePromise = undefined
  devicesServicePromise = undefined
  distributorsServicePromise = undefined
  distributorsDomainsServicePromise = undefined
  sweet = undefined
  serviceInjection = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _TenantsService_, _DevicesService_, _DistributorsService_, _$state_, _sweet_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    TenantsService = _TenantsService_
    DevicesService = _DevicesService_
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
    }

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      devicesServicePromise = new skykitDisplayDeviceManagement.q.Mock
      distributorsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      distributorsDomainsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise)
      spyOn(DevicesService, 'getDevicesByTenant').and.returnValue(devicesServicePromise)
      spyOn(DistributorsService, 'getByName').and.returnValue(distributorsServicePromise)
      spyOn(DistributorsService, 'getDomainsByKey').and.returnValue(distributorsDomainsServicePromise)

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
      expect(controller.currentTenant.domain_name).toBeUndefined()
      expect(controller.currentTenant.active).toBeTruthy()

    it 'defaultDistributor property should be Agosto', ->
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      expect(controller.defaultDistributorName).toEqual 'Agosto'

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

        beforeEach ->
          $stateParams = {}
          controller = $controller 'TenantDetailsCtrl', serviceInjection

        it 'sets general tab active to false', ->
          expect(controller.generalTabActive).toBeFalsy()

        it 'sets linked displays tab active to true', ->
          expect(controller.linkedDisplaysTabActive).toBeTruthy()

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

        beforeEach ->
          $stateParams = {}
          controller = $controller 'TenantDetailsCtrl', serviceInjection

        it 'sets general tab active to true', ->
          expect(controller.generalTabActive).toBeTruthy()

        it 'sets linked displays tab active to false', ->
          expect(controller.linkedDisplaysTabActive).toBeFalsy()

    describe '.initialize', ->
      beforeEach ->
        controller = $controller 'TenantDetailsCtrl', serviceInjection

      it 'calls DistributorsService.getByName to retrieve default distributor', ->
        controller.initialize()
        expect(DistributorsService.getByName).toHaveBeenCalledWith(controller.defaultDistributorName)

  describe '.onClickSaveButton', ->
    domain_name = undefined
    domain_key = undefined

    beforeEach ->
      tenantsServicePromise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(TenantsService, 'save').and.returnValue(tenantsServicePromise)
      spyOn($state, 'go')
      $stateParams = {}
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      controller = $controller 'TenantDetailsCtrl', serviceInjection
      domain_name = 'dev.agosto.com'
      domain_key = '123456789'
      controller.currentTenant.chrome_device_domain = {name: domain_name, key: domain_key}
      controller.onClickSaveButton()
      tenantsServicePromise.resolve()

    it 'start the progress bar animation', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call TenantsService.save, pass the current tenant', ->
      expect(TenantsService.save).toHaveBeenCalledWith(controller.currentTenant)

    it "the 'then' handler routes navigation back to 'tenants'", ->
      expect($state.go).toHaveBeenCalledWith('tenants')

    it 'the domain key gets set', ->
      expect(controller.currentTenant.domain_key).toBe domain_key

    it 'the domain name gets set', ->
      expect(controller.currentTenant.domain_name).toBe domain_name

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
