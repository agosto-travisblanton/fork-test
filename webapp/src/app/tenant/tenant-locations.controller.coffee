'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationsCtrl',
  ($scope, $stateParams, TenantsService, LocationsService, $state, ProgressBarService) ->
    vm = @
    tenantKey = $stateParams.tenantKey
    vm.currentTenant = undefined
    $scope.tabIndex = 3

    $scope.$watch 'tabIndex', (selectedIndex) ->
      if selectedIndex != undefined
        switch selectedIndex
          when 0
            $state.go 'tenantDetails', {tenantKey: tenantKey}
          when 1
            $state.go 'tenantManagedDevices', {tenantKey: tenantKey}
          when 2
            $state.go 'tenantUnmanagedDevices', {tenantKey: tenantKey}
          when 3
            $state.go 'tenantLocations', {tenantKey: tenantKey}


    vm.getLocations = (tenantKey, prev, next) ->
      ProgressBarService.start()
      locationsPromise = LocationsService.getLocationsByTenantKeyPaginated tenantKey, prev, next
      locationsPromise.then (data) ->
        vm.locations = data.locations
        vm.next_cursor = data.next_cursor
        vm.prev_cursor = data.prev_cursor
        ProgressBarService.complete()


    vm.paginateCall = (forward) ->
      if forward
        vm.getLocations tenantKey, null, vm.next_cursor

      else
        vm.getLocations tenantKey, vm.prev_cursor, null


    vm.initialize = ->
      vm.locations = []
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (data) ->
        vm.currentTenant = data
      vm.getLocations tenantKey

    vm.editItem = (item) ->
      $state.go 'editLocation', {locationKey: item.key}


    vm
