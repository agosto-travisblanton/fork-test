'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantDetailsCtrl',
  ($log, $stateParams, TenantsService, DomainsService, DevicesService, DistributorsService, $state, sweet,
    ProgressBarService, $cookies, $mdDialog, $scope) ->
    @currentTenant = {
      key: undefined,
      name: undefined,
      tenant_code: undefined,
      admin_email: undefined,
      content_server_url: undefined,
      content_manager_base_url: undefined,
      domain_key: undefined,
      notification_emails: undefined,
      proof_of_play_logging: false,
      active: true
    }
    @selectedDomain = undefined
    @distributorDomains = []
    @editMode = !!$stateParams.tenantKey

    if @editMode
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (tenant) =>
        @currentTenant = tenant
        @onSuccessResolvingTenant tenant

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
        sweet.show('Oops...',
          'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error')
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

    $scope.tabIndex = 0

    $scope.$watch 'tabIndex', (toTab, fromTab) ->

      if toTab != undefined
        switch toTab
          when 0
            $state.go 'tenantDetails', {tenantKey: $stateParams.tenantKey}
          when 1
            $state.go 'tenantManagedDevices', {tenantKey: $stateParams.tenantKey}
          when 2
            $state.go 'tenantUnmanagedDevices', {tenantKey: $stateParams.tenantKey}
          when 3
            $state.go 'tenantLocations', {tenantKey: $stateParams.tenantKey}

    @
