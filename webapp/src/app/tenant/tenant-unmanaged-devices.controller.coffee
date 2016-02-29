'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantUnmanagedDevicesCtrl',
  ($scope, $stateParams, TenantsService, DevicesService, $state) ->
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
    @tenantDevices = []
    @editMode = !!$stateParams.tenantKey

    if @editMode
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (tenant) =>
        @currentTenant = tenant
      devicesPromise = DevicesService.getUnmanagedDevicesByTenant $stateParams.tenantKey
      devicesPromise.then (data) =>
        @tenantDevices = data.objects

    $scope.tabIndex = 2

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

    @editItem = (item) ->
      $state.go 'editDevice', {deviceKey: item.key, tenantKey: $stateParams.tenantKey, fromDevices: false}

    @
