'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantAddCtrl',
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

    @initialize = ->
      @currentDistributorKey = $cookies.get('currentDistributorKey')
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
