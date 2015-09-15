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
    distributorPromise = DistributorsService.getByName(@defaultDistributorName)
    distributorPromise.then (data) =>
      distributor_key = data[0].key
      @onSuccessResolvingDistributor(distributor_key)

  @onSuccessResolvingDistributor = (distributor_key) =>
    distributorDomainPromise = DistributorsService.getDomainsByKey(distributor_key)
    distributorDomainPromise.then (domains_array) =>
      i = 0
      while i < domains_array.length
        domain = {name: domains_array[i].name, value: domains_array[i].name}
        @distributorDomains.push domain
        i++

  @onClickSaveButton = ->
    ProgressBarService.start()
    @currentTenant.chrome_device_domain = @currentTenant.chrome_device_domain.value
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
