'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantDetailsCtrl',
  ($log, $stateParams, TenantsService, DomainsService, DevicesService, DistributorsService, $state, sweet,
    ProgressBarService, $cookies, $mdDialog) ->
    @currentTenant = {
      key: undefined,
      name: undefined,
      tenant_code: undefined,
      admin_email: undefined,
      content_server_url: undefined,
      content_manager_base_url: undefined,
      domain_key: undefined,
      notification_emails: undefined,
      active: true
    }
    @selectedDomain = undefined
    @currentTenantDisplays = []
    @currentTenantUnmanagedDisplays = []
    @distributorDomains = []
    @editMode = !!$stateParams.tenantKey

    if @editMode
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (tenant) =>
        @currentTenant = tenant
        @onSuccessResolvingTenant tenant
      devicesPromise = DevicesService.getDevicesByTenant $stateParams.tenantKey
      devicesPromise.then (data) =>
        @currentTenantDisplays = data.objects

      unmanagedDevicesPromise = DevicesService.getUnmanagedDevicesByTenant $stateParams.tenantKey
      unmanagedDevicesPromise.then (data) =>
        @currentTenantUnmanagedDisplays = data.objects

    @initialize = ->
      @currentDistributorKey = $cookies.get('currentDistributorKey')
      distributorDomainPromise = DistributorsService.getDomainsByKey @currentDistributorKey
      distributorDomainPromise.then (domains) =>
        @distributorDomains = domains

    @onSuccessResolvingTenant = (tenant) =>
      domainPromise = DomainsService.getDomainByKey tenant.domain_key
      domainPromise.then (data) =>
        @selectedDomain = data

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
      if errorObject.status is 409
        sweet.show('Oops...', 'Tenant code unavailable. Please try a different tenant code.', 'error')
      else
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

    @showDeviceDetails = (item, event) ->
      apiKey = item.apiKey
      $mdDialog.show($mdDialog.alert()
        .title('Device Details')
        .textContent("API key: #{apiKey}")
        .ariaLabel('Device details')
        .ok('Close')
        .targetEvent(event))

    @
