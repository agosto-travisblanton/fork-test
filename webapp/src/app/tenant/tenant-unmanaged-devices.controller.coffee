'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantUnmanagedDevicesCtrl',
  ($scope, $stateParams, TenantsService, DevicesService, ProgressBarService, $state) ->
    vm = @
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
      active: true
    }
    vm.tenantDevices = []
    vm.devicesPrev = null
    vm.devicesNext = null
    vm.selectedButton = "MAC"
    vm.serialDevices = {}
    vm.disabled = true
    vm.macDevices = {}
    vm.editMode = !!$stateParams.tenantKey
    vm.tenantKey = $stateParams.tenantKey

    vm.getUnmanagedDevices = (tenantKey, prev_cursor, next_cursor) ->
      ProgressBarService.start()
      devicesPromise = DevicesService.getUnmanagedDevicesByTenant tenantKey, prev_cursor, next_cursor
      devicesPromise.then (data) ->
        vm.devicesPrev = data["prev_cursor"]
        vm.devicesNext = data["next_cursor"]
        vm.tenantDevices = data["devices"]
        ProgressBarService.complete()

    vm.refreshDevices = () ->
      vm.devicesPrev = null
      vm.devicesNext = null
      vm.tenantDevices = null
      DevicesService.deviceByTenantCache.removeAll()
      vm.getUnmanagedDevices vm.tenantKey, vm.devicesPrev, vm.devicesNext

    if vm.editMode
      tenantPromise = TenantsService.getTenantByKey vm.tenantKey
      tenantPromise.then (tenant) ->
        vm.currentTenant = tenant

      vm.getUnmanagedDevices vm.tenantKey, null, null

    $scope.tabIndex = 2

    $scope.$watch 'tabIndex', (toTab, fromTab) ->
      if toTab != undefined
        switch toTab
          when 0
            $state.go 'tenantDetails', {tenantKey: vm.tenantKey}
          when 1
            $state.go 'tenantManagedDevices', {tenantKey: vm.tenantKey}
          when 2
            $state.go 'tenantUnmanagedDevices', {tenantKey: vm.tenantKey}
          when 3
            $state.go 'tenantLocations', {tenantKey: vm.tenantKey}

    vm.editItem = (item) ->
      $state.go 'editDevice', {deviceKey: item.key, tenantKey: vm.tenantKey, fromDevices: false}


    vm.convertArrayToDictionary = (theArray, mac) ->
      Devices = {}
      for item in theArray
        if mac
          Devices[item.mac] = item
        else
          Devices[item.serial] = item
      return Devices

    vm.changeRadio = () ->
      vm.searchText = ''
      vm.disabled = true
      vm.serialDevices = {}
      vm.macDevices = {}


    vm.searchDevices = (partial_search) ->
      if partial_search
        if partial_search.length > 2
          if vm.selectedButton == "Serial Number"
            DevicesService.searchDevicesByPartialSerialByTenant(vm.tenantKey, partial_search, true)
            .then (res) ->
              result = res["serial_number_matches"]
              vm.serialDevices = vm.convertArrayToDictionary(result, false)
              return [each.serial for each in result][0]

          else
            DevicesService.searchDevicesByPartialMacByTenant(vm.tenantKey, partial_search, true)
            .then (res) ->
              result = res["mac_matches"]
              vm.macDevices = vm.convertArrayToDictionary(result, true)
              return [each.mac for each in result][0]
        else
          return []
      else
        return []

    vm.paginateCall = (forward) ->
      if forward
        vm.getUnmanagedDevices vm.tenantKey, null, vm.devicesNext

      else
        vm.getUnmanagedDevices vm.tenantKey, vm.devicesPrev, null


    vm.prepareForEditView = (searchText) ->
      mac = vm.selectedButton == "MAC"
      if mac
        vm.editItem vm.macDevices[searchText]
      else
        vm.editItem vm.serialDevices[searchText]


    vm.controlOpenButton = (isMatch) ->
      vm.disabled = !isMatch
      vm.loadingDisabled = false

    vm.isResourceValid = (resource) ->
      if resource
        if resource.length > 2
          mac = vm.selectedButton == "MAC"
          vm.loadingDisabled = true

          if mac
            DevicesService.matchDevicesByFullMacByTenant(vm.tenantKey, resource, true)
            .then (res) ->
              vm.controlOpenButton(res["is_match"])

          else
            DevicesService.matchDevicesByFullSerialByTenant(vm.tenantKey, resource, true)
            .then (res) ->
              vm.controlOpenButton(res["is_match"])

        else
          vm.controlOpenButton(false)

      else
        vm.controlOpenButton(false)

    vm




