'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantAddCtrl',
  ($log, $location, TenantsService, DistributorsService, TimezonesService, $state, sweet, ProgressBarService,
    SessionsService) ->
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

    vm.initialize = ->
      timezonePromise = TimezonesService.getUsTimezones()
      timezonePromise.then (data) ->
        vm.timezones = data
      vm.currentDistributorKey = SessionsService.getCurrentDistributorKey()
      distributorPromise = DistributorsService.getByKey vm.currentDistributorKey
      distributorPromise.then (data) ->
        vm.currentTenant.content_manager_base_url = data.content_manager_url
        vm.currentTenant.content_server_url = data.player_content_url
      distributorDomainPromise = DistributorsService.getDomainsByKey vm.currentDistributorKey
      distributorDomainPromise.then (domains) ->
        vm.distributorDomains = domains

    vm.onClickSaveButton = ->
      ProgressBarService.start()
      vm.currentTenant.default_timezone = vm.selectedTimezone
      vm.currentTenant.domain_key = vm.selectedDomain.key
      promise = TenantsService.save vm.currentTenant
      promise.then vm.onSuccessTenantSave, vm.onFailureTenantSave

    vm.onSuccessTenantSave = ->
      ProgressBarService.complete()
      $state.go 'tenants'

    vm.onFailureTenantSave = (errorObject) ->
      ProgressBarService.complete()
      if errorObject.status is 409
        sweet.show('Oops...',
          'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error')
      else
        $log.error errorObject
        sweet.show('Oops...', 'Unable to save the tenant.', 'error')

    vm.autoGenerateTenantCode = ->
      unless vm.currentTenant.key
        newTenantCode = ''
        if vm.currentTenant.name
          newTenantCode = vm.currentTenant.name.toLowerCase()
          newTenantCode = newTenantCode.replace(/\s+/g, '_')
          newTenantCode = newTenantCode.replace(/\W+/g, '')
        vm.currentTenant.tenant_code = newTenantCode

    vm
