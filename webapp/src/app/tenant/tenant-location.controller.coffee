'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationCtrl',
  ($log, $stateParams, TenantsService, LocationsService, $state, sweet, ProgressBarService, $timeout) ->
    tenantKey = $stateParams.tenantKey
    @selectedTimezone = undefined
    @editMode = !!$stateParams.locationKey
    if @editMode
      locationPromise = LocationsService.getLocationByKey $stateParams.locationKey
      locationPromise.then (data) =>
        @location = data
        @selectedTimezone = data.timezone
        @tenantKey = data.tenantKey
        @fetchTenantName @tenantKey
    @timezones = []

    @initialize = ->
      timezonePromise = LocationsService.getTimezones()
      timezonePromise.then (data) =>
        @timezones = data
      if not @editMode
        @selectedTimezone = 'America/Chicago'
        @fetchTenantName tenantKey
        @location = {
          tenantKey: tenantKey
          active: true
        }

    @onClickSaveButton = ->
      ProgressBarService.start()
      @location.timezone = @selectedTimezone
      promise = LocationsService.save @location
      promise.then @onSuccessLocationSave(@tenantKey), @onFailureLocationSave

    @onSuccessLocationSave = (tenantKey)->
      ProgressBarService.complete()
      setTimeout (->
        $state.go 'tenantLocations', {tenantKey: tenantKey}
        return
      ), 1000

    @onFailureLocationSave = (errorObject) ->
      ProgressBarService.complete()
      $log.error errorObject
      sweet.show('Oops...', 'Unable to save the location.', 'error')

    @fetchTenantName = (tenantKey) =>
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (tenant) =>
        @tenantName = tenant.name

    @
