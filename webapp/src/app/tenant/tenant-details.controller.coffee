'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'TenantDetailsCtrl', ($log,
                                           $stateParams,
                                           TenantsService,
                                           DomainsService,
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
    domain_key: undefined
    active: true
  }
  @selectedDomain = undefined
  @defaultDistributorName = 'Agosto'
  @currentTenantDisplays = []
  @distributorDomains = []
  @editMode = !!$stateParams.tenantKey

  if @editMode
    tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
    tenantPromise.then (tenant) =>
      @currentTenant = tenant
      @onSuccessResolvingTenant tenant
    displaysPromise = DevicesService.getDevicesByTenant $stateParams.tenantKey
    displaysPromise.then (data) =>
      @currentTenantDisplays = data.objects

  @initialize = ->
    distributorPromise = DistributorsService.getByName @defaultDistributorName
    distributorPromise.then (data) =>
      distributor_key = data[0].key
      @onSuccessResolvingDistributor distributor_key

  @onSuccessResolvingTenant = (tenant) =>
    domainPromise = DomainsService.getDomainByKey tenant.domain_key
    domainPromise.then (data) =>
      @selectedDomain = data

  @onSuccessResolvingDistributor = (distributor_key) =>
    distributorDomainPromise = DistributorsService.getDomainsByKey distributor_key
    distributorDomainPromise.then (domains) =>
      @distributorDomains = domains

  @onClickSaveButton = ->
    ProgressBarService.start()
    @currentTenant.domain_key = @selectedDomain.key
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

  @autoGenerateTenantCode = ->
    unless @currentTenant.key
      newTenantCode = ''
      if @currentTenant.name
        newTenantCode = @currentTenant.name.toLowerCase()
        newTenantCode = newTenantCode.replace(/\s+/g, '_')
        newTenantCode = newTenantCode.replace(/\W+/g, '')
      @currentTenant.tenant_code = newTenantCode

  @
