'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantManagedDevicesCtrl', ($scope, $stateParams, TenantsService, DevicesService, $state) ->
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


  @getManagedDevices = (tenantKey, prev_cursor, next_cursor) ->
    devicesPromise = DevicesService.getDevicesByTenant tenantKey, prev_cursor, next_cursor
    devicesPromise.then (data) =>
      @devicesPrev = data["prev_cursor"]
      @devicesNext = data["next_cursor"]
      @tenantDevices = data["devices"]


  if @editMode
    tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
    tenantPromise.then (tenant) =>
      @currentTenant = tenant

    @getManagedDevices $stateParams.tenantKey, null, null


  @paginateCall = (forward) ->
    if forward
      @getManagedDevices $stateParams.tenantKey, null, @devicesNext

    else
      @getManagedDevices $stateParams.tenantKey, @devicesPrev, null

  $scope.tabIndex = 1

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
