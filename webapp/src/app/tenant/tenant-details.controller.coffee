'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantDetailsCtrl',
  ($stateParams, TenantsService, DomainsService, TimezonesService, DistributorsService, $state, sweet,
    ProgressBarService, ToastsService, $cookies, $scope, $location) ->
    @gameStopServer = $location.host().indexOf('provisioning-gamestop') > -1
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
      proof_of_play_url: undefined,
      active: true
    }
    @selectedDomain = undefined
    @distributorDomains = []
    @timezones = []
    @selectedTimezone = 'America/Chicago'
    @editMode = !!$stateParams.tenantKey

    if @editMode
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (tenant) =>
        @currentTenant = tenant
        @onSuccessResolvingTenant tenant

    @initialize = ->
      timezonePromise = TimezonesService.getUsTimezones()
      timezonePromise.then (data) =>
        @timezones = data
      @currentDistributorKey = $cookies.get('currentDistributorKey')
      distributorDomainPromise = DistributorsService.getDomainsByKey @currentDistributorKey
      distributorDomainPromise.then (domains) =>
        @distributorDomains = domains

    @onSuccessResolvingTenant = (tenant) =>
      @selectedTimezone = tenant.default_timezone
      domainPromise = DomainsService.getDomainByKey tenant.domain_key
      domainPromise.then (data) =>
        @selectedDomain = data

    @onClickSaveButton = ->
      ProgressBarService.start()
      @currentTenant.default_timezone = @selectedTimezone
      @currentTenant.domain_key = @selectedDomain.key
      promise = TenantsService.save @currentTenant
      promise.then @onSuccessTenantSave, @onFailureTenantSave

    @onSuccessTenantSave = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We saved your tenant information.'
      $state.go 'tenants'

    @onFailureTenantSave = (errorObject) ->
      ProgressBarService.complete()
      if errorObject.status is 409
        sweet.show('Oops...',
          'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error')
      else
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
