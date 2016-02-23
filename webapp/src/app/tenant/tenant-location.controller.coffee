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
        tenantPromise = TenantsService.getTenantByKey @location.tenantKey
        tenantPromise.then (tenant) =>
          @tenantName = tenant.name
    else
      @location = {
        tenantKey: $stateParams.tenantKey
        active: true
      }
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (tenant) =>
        @tenantName = tenant.name

    @onClickSaveButton = ->
      ProgressBarService.start()
      promise = LocationsService.save @location
      promise.then @onSuccessLocationSave, @onFailureLocationSave

    @onSuccessLocationSave = ->
      ProgressBarService.complete()
      $state.go 'tenantLocations', {tenantKey: $stateParams.tenantKey}

    @onFailureLocationSave = (errorObject) ->
      ProgressBarService.complete()
      $log.error errorObject
      sweet.show('Oops...', 'Unable to save the location.', 'error')

    @
