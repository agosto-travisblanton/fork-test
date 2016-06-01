'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantDetailsCtrl',
  ($stateParams, TenantsService, DomainsService, TimezonesService, DistributorsService, $state, sweet,
    ProgressBarService, ToastsService, SessionsService, $scope, $location) ->
    vm = @
    vm.gameStopServer = $location.host().indexOf('provisioning-gamestop') > -1
    vm.currentTenant = {
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
    vm.selectedDomain = undefined
    vm.distributorDomains = []
    vm.timezones = []
    vm.selectedTimezone = 'America/Chicago'
    vm.editMode = !!$stateParams.tenantKey

    if vm.editMode
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (tenant) ->
        vm.currentTenant = tenant
        vm.onSuccessResolvingTenant tenant

    vm.initialize = ->
      timezonePromise = TimezonesService.getCustomTimezones()
      timezonePromise.then (data) ->
        vm.timezones = data
      vm.currentDistributorKey = SessionsService.getCurrentDistributorKey()
      distributorDomainPromise = DistributorsService.getDomainsByKey vm.currentDistributorKey
      distributorDomainPromise.then (domains) ->
        vm.distributorDomains = domains

    vm.onSuccessResolvingTenant = (tenant) ->
      vm.selectedTimezone = tenant.default_timezone
      domainPromise = DomainsService.getDomainByKey tenant.domain_key
      domainPromise.then (data) ->
        vm.selectedDomain = data

    vm.onClickSaveButton = ->
      ProgressBarService.start()
      vm.currentTenant.default_timezone = vm.selectedTimezone
      vm.currentTenant.domain_key = vm.selectedDomain.key
      promise = TenantsService.save vm.currentTenant
      promise.then vm.onSuccessTenantSave, vm.onFailureTenantSave

    vm.onSuccessTenantSave = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We saved your tenant information.'

    vm.onFailureTenantSave = (errorObject) ->
      ProgressBarService.complete()
      if errorObject.status is 409
        sweet.show('Oops...',
          'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error')
      else
        sweet.show('Oops...', 'Unable to save the tenant.', 'error')

    vm.editItem = (item) ->
      $state.go 'editDevice', {deviceKey: item.key, tenantKey: $stateParams.tenantKey}

    vm.autoGenerateTenantCode = ->
      unless vm.currentTenant.key
        newTenantCode = ''
        if vm.currentTenant.name
          newTenantCode = vm.currentTenant.name.toLowerCase()
          newTenantCode = newTenantCode.replace(/\s+/g, '_')
          newTenantCode = newTenantCode.replace(/\W+/g, '')
        vm.currentTenant.tenant_code = newTenantCode

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

    vm
