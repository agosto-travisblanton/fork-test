'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'TenantDetailsCtrl', ($log,
                                           $stateParams,
                                           TenantsService,
                                           DevicesService,
                                           DistributorsService,
                                           $state,
                                           sweet,
                                           ProgressBarService) ->
  @currentTenant = {
    key: undefined,
    name: undefined,
    tenant_code: undefined,
    admin_email: undefined,
    content_server_url: undefined,
    content_manager_base_url: undefined,
    chrome_device_domain: undefined,
    active: true
  }
  @defaultDistributorName = 'Agosto'
  @defaultDistributor = undefined
  @currentTenantDisplays = []
  @distributorDomains = []
  @editMode = !!$stateParams.tenantKey

  if @editMode
    @generalTabActive = false
    @linkedDisplaysTabActive = true
    tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey)
    tenantPromise.then (data) =>
      @currentTenant = data

    displaysPromise = DevicesService.getDevicesByTenant($stateParams.tenantKey)
    displaysPromise.then (data) =>
      @currentTenantDisplays = data.objects
  else
    @generalTabActive = true
    @linkedDisplaysTabActive = false

  @initialize = ->
    @distributorDomains = [
      {name : 'looks.agosto.com', key: '1111111'}
      {name : 'local.agosto.com', key: '2222221'}
    ]

    distributorPromise = DistributorsService.getByName(@defaultDistributorName)
    distributorPromise.then (data) =>
      @defaultDistributor = data
      distributorDomainPromise = DistributorsService.getDomainsByKey(data[0].key)
      distributorDomainPromise.then (data) =>
        @distributorDomains = data

  @onClickSaveButton = ->
    ProgressBarService.start()
    @currentTenant.chrome_device_domain = @currentTenant.chrome_device_domain.key
    promise = TenantsService.save @currentTenant
    promise.then @onSuccessTenantSave, @onFailureTenantSave

  @onSuccessTenantSave = ->
    ProgressBarService.complete()
    $state.go 'tenants'

  @onFailureTenantSave = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the tenant.', 'error')

  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantKey: $stateParams.tenantKey}

  @selectDomain = ->


  @autoGenerateTenantCode = ->
    unless @currentTenant.key
      newTenantCode = ''
      if @currentTenant.name
        newTenantCode = @currentTenant.name.toLowerCase()
        newTenantCode = newTenantCode.replace(/\s+/g, '_')
        newTenantCode = newTenantCode.replace(/\W+/g, '')
      @currentTenant.tenant_code = newTenantCode

  @
