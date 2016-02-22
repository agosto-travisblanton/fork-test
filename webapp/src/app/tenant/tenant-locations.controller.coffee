'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationsCtrl',
  ($scope, $stateParams, TenantsService, DomainsService, DevicesService, DistributorsService, $state, sweet,
    ProgressBarService, $cookies, $mdDialog) ->
    @currentTenantLocations = []
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
    @editMode = !!$stateParams.tenantKey

    if @editMode
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (tenant) =>
        @currentTenant = tenant

    $scope.tabIndex = 3

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
