'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationsCtrl',
  ($scope, $stateParams, TenantsService, LocationsService, $state) ->
    @locations = []
    @currentTenant = undefined

    @initialize = ->
      tenantPromise = TenantsService.getTenantByKey $stateParams.tenantKey
      tenantPromise.then (data) =>
        @currentTenant = data
      locationsPromise = LocationsService.getLocationsByTenantKey $stateParams.tenantKey
      locationsPromise.then (data) =>
        @locations = data

    @editItem = (item) ->
      $state.go 'editLocation', {locationKey: item.key}

    $scope.tabIndex = 3

    $scope.$watch 'tabIndex', (selectedIndex) ->
      if selectedIndex != undefined
        switch selectedIndex
          when 0
            $state.go 'tenantDetails', {tenantKey: $stateParams.tenantKey}
          when 1
            $state.go 'tenantManagedDevices', {tenantKey: $stateParams.tenantKey}
          when 2
            $state.go 'tenantUnmanagedDevices', {tenantKey: $stateParams.tenantKey}
          when 3
            $state.go 'tenantLocations', {tenantKey: $stateParams.tenantKey}

    @
