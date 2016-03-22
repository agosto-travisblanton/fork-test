'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantAddCtrl',
  ($log, $location, TenantsService, DistributorsService, $state, sweet, ProgressBarService, $cookies) ->
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

    @initialize = ->
      @currentDistributorKey = $cookies.get('currentDistributorKey')
      distributorPromise = DistributorsService.getByKey @currentDistributorKey
      distributorPromise.then (data) =>
        @currentTenant.content_server_url = data.player_content_url
        @currentTenant.content_manager_base_url = data.content_manager_url
      distributorDomainPromise = DistributorsService.getDomainsByKey @currentDistributorKey
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
      if errorObject.status is 409
        sweet.show('Oops...',
          'Tenant code unavailable. Please modify tenant name to generate a unique tenant code.', 'error')
      else
        $log.error errorObject
        sweet.show('Oops...', 'Unable to save the tenant.', 'error')

    @autoGenerateTenantCode = ->
      unless @currentTenant.key
        newTenantCode = ''
        if @currentTenant.name
          newTenantCode = @currentTenant.name.toLowerCase()
          newTenantCode = newTenantCode.replace(/\s+/g, '_')
          newTenantCode = newTenantCode.replace(/\W+/g, '')
        @currentTenant.tenant_code = newTenantCode

    @
