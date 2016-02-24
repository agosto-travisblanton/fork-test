'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationsCtrl',
  ($scope, $stateParams, TenantsService, LocationsService, $state) ->
    tenantKey = $stateParams.tenantKey
    @locations = []
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

    @initialize = ->
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (data) =>
        @currentTenant = data
      locationsPromise = LocationsService.getLocationsByTenantKey tenantKey
      locationsPromise.then (data) =>
        @locations = data

    @editItem = (item) ->
      $state.go 'editLocation', {locationKey: item.key}


    @
