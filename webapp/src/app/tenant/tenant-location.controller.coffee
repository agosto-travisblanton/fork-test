'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantLocationCtrl',
  ($stateParams, TenantsService, LocationsService, $state, sweet, ProgressBarService, ToastsService) ->
    vm = @
    vm.location = {
      key: undefined
    }
    vm.tenantKey = $stateParams.tenantKey
    vm.editMode = !!$stateParams.locationKey
    if vm.editMode
      locationPromise = LocationsService.getLocationByKey $stateParams.locationKey
      locationPromise.then (data) ->
        vm.location = data
        vm.tenantKey = data.tenantKey
        vm.locationName = data.customerLocationName
        vm.fetchTenantName vm.tenantKey

    vm.initialize = ->
      if not vm.editMode
        vm.fetchTenantName vm.tenantKey
        vm.location = {
          tenantKey: vm.tenantKey
          active: true
        }

    vm.onClickSaveButton = ->
      ProgressBarService.start()
      promise = LocationsService.save vm.location
      if vm.editMode
        promise.then vm.onSuccessUpdatingLocation(vm.tenantKey), vm.onFailureSavingLocation
      else
        promise.then vm.onSuccessSavingLocation, vm.onFailureSavingLocation

    vm.onSuccessSavingLocation = ()->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We saved your location.'
      setTimeout (->
        $state.go 'tenantLocations', {tenantKey: $stateParams.tenantKey}
        return
      ), 1000

    vm.onSuccessUpdatingLocation = (tenant_key)->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We updated your location.'
      setTimeout (->
        $state.go 'tenantLocations', {tenantKey: tenant_key}
        return
      ), 1000

    vm.onFailureSavingLocation = (response) ->
      ProgressBarService.complete()
      if response.status is 409
        ToastsService.showErrorToast 'Location code conflict. Unable to save your location.'
        sweet.show('Oops...',
          'Please change your customer location name. Location name must generate a unique location code.',
          'error')
      else
        ToastsService.showErrorToast 'Unable to save your location.'

    vm.fetchTenantName = (tenantKey) ->
      tenantPromise = TenantsService.getTenantByKey tenantKey
      tenantPromise.then (tenant) ->
        vm.tenantName = tenant.name

    vm.autoGenerateCustomerLocationCode = ->
      unless vm.location.key
        newCustomerLocationCode = ''
        if vm.location.customerLocationName
          newCustomerLocationCode = vm.location.customerLocationName.toLowerCase()
          newCustomerLocationCode = newCustomerLocationCode.replace(/\s+/g, '_')
          newCustomerLocationCode = newCustomerLocationCode.replace(/\W+/g, '')
        vm.location.customerLocationCode = newCustomerLocationCode

    vm

