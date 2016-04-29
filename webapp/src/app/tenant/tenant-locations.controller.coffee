'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationsCtrl',
  ($scope, $stateParams, TenantsService, LocationsService, $state) ->
    tenantKey = $stateParams.tenantKey
    @currentTenant = undefined
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

    
    @getLocations = (tenantKey, prev, next) =>
      locationsPromise = LocationsService.getLocationsByTenantKey tenantKey, prev, next
      locationsPromise.then (data) =>
        console.log(data)
        @locations = data.locations
        @next_cursor = data.next_cursor
        @prev_cursor = data.prev_cursor

        
        
    @paginateCall = (forward) ->
      if forward
        @getLocations tenantKey, null, @next_cursor

      else
        @getLocations tenantKey, @prev_cursor, null


    @initialize = =>
      @locations = []
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (data) =>
        @currentTenant = data
      @getLocations tenantKey

    @editItem = (item) ->
      $state.go 'editLocation', {locationKey: item.key}


    @
