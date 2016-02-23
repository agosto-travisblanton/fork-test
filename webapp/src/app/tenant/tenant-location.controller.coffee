'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationCtrl',
  ($log, $stateParams, TenantsService, LocationsService, $state, sweet, ProgressBarService) ->
    tenantKey = $stateParams.tenantKey
    @editMode = !!$stateParams.locationKey
    if @editMode
      locationPromise = LocationsService.getLocationByKey $stateParams.locationKey
      locationPromise.then (data) =>
        @location = data
        @fetchTenantName data.tenantKey
    @timezones = []
    @selectedTimezone = 'America/Chicago'

    @initialize = ->
      timezonePromise = LocationsService.getTimezones()
      timezonePromise.then (data) =>
        @timezones = data
      if not @editMode
        @fetchTenantName tenantKey
        @location = {
          tenantKey: tenantKey
          active: true
        }

    @onClickSaveButton = ->
      ProgressBarService.start()
      @location.timezone = @selectedTimezone
      promise = LocationsService.save @location
      promise.then @onSuccessLocationSave, @onFailureLocationSave

    @onSuccessLocationSave = ->
      ProgressBarService.complete()
      $state.go 'tenantLocations', {tenantKey: $stateParams.tenantKey}

    @onFailureLocationSave = (errorObject) ->
      ProgressBarService.complete()
      $log.error errorObject
      sweet.show('Oops...', 'Unable to save the location.', 'error')

    @fetchTenantName = (tenantKey) =>
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (tenant) =>
        @tenantName = tenant.name

    @
