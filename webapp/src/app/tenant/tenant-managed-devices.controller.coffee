'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantManagedDevicesCtrl', ($scope, $stateParams, TenantsService, ProgressBarService, DevicesService, $state) ->
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
  @devicesPrev = null
  @devicesNext = null
  @selectedButton = "Serial Number"
  @serialDevices = {}
  @disabled = true
  @macDevices = {}
  @editMode = !!$stateParams.tenantKey
  @tenantKey = $stateParams.tenantKey

  $scope.tabIndex = 1

  $scope.$watch 'tabIndex', (toTab, fromTab) =>
    if toTab != undefined
      switch toTab
        when 0
          $state.go 'tenantDetails', {tenantKey: @tenantKey}
        when 1
          $state.go 'tenantManagedDevices', {tenantKey: @tenantKey}
        when 2
          $state.go 'tenantUnmanagedDevices', {tenantKey: @tenantKey}
        when 3
          $state.go 'tenantLocations', {tenantKey: @tenantKey}

  @getManagedDevices = (tenantKey, prev_cursor, next_cursor) ->
    ProgressBarService.start()
    devicesPromise = DevicesService.getDevicesByTenant tenantKey, prev_cursor, next_cursor
    devicesPromise.then (data) =>
      @devicesPrev = data["prev_cursor"]
      @devicesNext = data["next_cursor"]
      @tenantDevices = data["devices"]
      ProgressBarService.complete()

  if @editMode
    tenantPromise = TenantsService.getTenantByKey @tenantKey
    tenantPromise.then (tenant) =>
      @currentTenant = tenant

    @getManagedDevices @tenantKey, null, null


  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantKey: @tenantKey, fromDevices: false}


  @convertArrayToDictionary = (theArray, mac) ->
    Devices = {}
    for item in theArray
      if mac
        Devices[item.mac] = item
      else
        Devices[item.serial] = item
    return Devices

  @changeRadio = () =>
    @searchText = ''
    @disabled = true
    @serialDevices = {}
    @macDevices = {}


  @searchDevices = (partial_search) =>
    if partial_search
      if partial_search.length > 2
        if @selectedButton == "Serial Number"
          DevicesService.searchDevicesByPartialSerialByTenant(@tenantKey, partial_search, false)
          .then (res) =>
            result = res["serial_number_matches"]
            @serialDevices = @convertArrayToDictionary(result, false)
            return [each.serial for each in result][0]

        else
          DevicesService.searchDevicesByPartialMacByTenant(@tenantKey, partial_search, false)
          .then (res) =>
            result = res["mac_matches"]
            @macDevices = @convertArrayToDictionary(result, true)
            return [each.mac for each in result][0]

  @paginateCall = (forward) ->
    if forward
      @getManagedDevices @tenantKey, null, @devicesNext

    else
      @getManagedDevices @tenantKey, @devicesPrev, null


  @prepareForEditView = (searchText) ->
    mac = @selectedButton == "MAC"
    if mac
      @editItem @macDevices[searchText]
    else
      @editItem @serialDevices[searchText]


  @controlOpenButton = (isMatch) =>
    @disabled = !isMatch


  @isResourceValid = (resource) ->
    if resource
      if resource.length > 2
        mac = @selectedButton == "MAC"

        if mac
          DevicesService.matchDevicesByFullMacByTenant(@tenantKey, resource, false)
          .then (res) =>
            @controlOpenButton(res["is_match"])

        else
          DevicesService.matchDevicesByFullSerialByTenant(@tenantKey, resource, false)
          .then (res) =>
            @controlOpenButton(res["is_match"])

      else
        @controlOpenButton(false)

    else
      @controlOpenButton(false)

  @
