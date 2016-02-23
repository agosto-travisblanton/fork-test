'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationCtrl',
  ($log, $stateParams, TenantsService, LocationsService, $state, sweet, ProgressBarService, $timeout) ->
    @tenantKey = $stateParams.tenantKey
    @selectedTimezone = 'America/Chicago'
    @editMode = !!$stateParams.locationKey
    if @editMode
      locationPromise = LocationsService.getLocationByKey $stateParams.locationKey
      locationPromise.then (data) =>
        @location = data
        @selectedTimezone = data.timezone
        @tenantKey = data.tenantKey
        @locationName = data.customerLocationName
        @fetchTenantName @tenantKey
    @timezones = []

    @initialize = ->
      timezonePromise = LocationsService.getTimezones()
      timezonePromise.then (data) =>
        @timezones = data
      if not @editMode
        @fetchTenantName @tenantKey
        @location = {
          tenantKey: @tenantKey
          active: true
        }

    @onClickSaveButton = ->
      ProgressBarService.start()
      @location.timezone = @selectedTimezone
      promise = LocationsService.save @location
      promise.then @onSuccessSavingLocation(@tenantKey), @onFailureSavingLocation

    @onSuccessSavingLocation = (tenantKey)->
      ProgressBarService.complete()
      setTimeout (->
        $state.go 'tenantLocations', {tenantKey: tenantKey}
        return
      ), 1000

    @onFailureSavingLocation = (errorObject) ->
      ProgressBarService.complete()
      $log.error errorObject
      sweet.show('Oops...', 'Unable to save the location.', 'error')

    @fetchTenantName = (tenantKey) =>
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (tenant) =>
        @tenantName = tenant.name

    @autoGenerateCustomerLocationCode = ->
      unless @location.key
        newCustomerLocationCode = ''
        if @location.customerLocationName
          newCustomerLocationCode = @location.customerLocationName.toLowerCase()
          newCustomerLocationCode = newCustomerLocationCode.replace(/\s+/g, '_')
          newCustomerLocationCode = newCustomerLocationCode.replace(/\W+/g, '')
        @location.customerLocationCode = newCustomerLocationCode


    @
