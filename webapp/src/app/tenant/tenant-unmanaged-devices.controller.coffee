'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantUnmanagedDevicesCtrl',
  ($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) ->
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
    @selectedButton = "MAC"
    @serialDevices = {}
    @disabled = true
    @macDevices = {}
    @editMode = !!$stateParams.tenantKey
    @tenantKey = $stateParams.tenantKey

    @getManagedDevices = (tenantKey, prev_cursor, next_cursor) ->
      ProgressBarService.start()
      devicesPromise = DevicesService.getUnmanagedDevicesByTenant tenantKey, prev_cursor, next_cursor
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

    $scope.tabIndex = 2

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
            DevicesService.searchDevicesByPartialSerialByTenant(@tenantKey, partial_search, true)
            .then (res) =>
              result = res["serial_number_matches"]
              @serialDevices = @convertArrayToDictionary(result, false)
              return [each.serial for each in result][0]

          else
            DevicesService.searchDevicesByPartialMacByTenant(@tenantKey, partial_search, true)
            .then (res) =>
              result = res["mac_matches"]
              @macDevices = @convertArrayToDictionary(result, true)
              return [each.mac for each in result][0]
        else
          return []
      else 
        return []
        
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
            DevicesService.matchDevicesByFullMacByTenant(@tenantKey, resource, true)
            .then (res) =>
              @controlOpenButton(res["is_match"])

          else
            DevicesService.matchDevicesByFullSerialByTenant(@tenantKey, resource, true)
            .then (res) =>
              @controlOpenButton(res["is_match"])

        else
          @controlOpenButton(false)

      else
        @controlOpenButton(false)

    @




