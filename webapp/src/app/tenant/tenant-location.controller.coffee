'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationCtrl',
  ($stateParams, TenantsService, LocationsService, $state, sweet, ProgressBarService, ToastsService) ->
    @location = {
      key: undefined
    }
    @tenantKey = $stateParams.tenantKey
    @editMode = !!$stateParams.locationKey
    if @editMode
      locationPromise = LocationsService.getLocationByKey $stateParams.locationKey
      locationPromise.then (data) =>
        @location = data
        @tenantKey = data.tenantKey
        @locationName = data.customerLocationName
        @fetchTenantName @tenantKey

    @initialize = ->
      if not @editMode
        @fetchTenantName @tenantKey
        @location = {
          tenantKey: @tenantKey
          active: true
        }

    @onClickSaveButton = ->
      ProgressBarService.start()
      promise = LocationsService.save @location
      promise.then @onSuccessSavingLocation, @onFailureSavingLocation

    @onSuccessSavingLocation = ()->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We saved your location.'
      setTimeout (->
        $state.go 'tenantLocations', {tenantKey: $stateParams.tenantKey}
        return
      ), 1000

    @onFailureSavingLocation = (response) ->
      ProgressBarService.complete()
      if response.status is 409
        ToastsService.showErrorToast 'Location code conflict. Unable to save your location.'
        sweet.show('Oops...',
          'Please change your customer location name. Location name must generate a unique location code.',
          'error')
      else
        ToastsService.showErrorToast 'Unable to save your location.'

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

