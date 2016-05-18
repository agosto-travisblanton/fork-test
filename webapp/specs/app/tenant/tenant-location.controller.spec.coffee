'use strict'

describe 'TenantLocationCtrl', ->
  scope = undefined
  sweet = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  LocationsService = undefined
  ToastsService = undefined
  serviceInjection = undefined
  tenantsServicePromise = undefined
  locationsServicePromise = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _TenantsService_, _LocationsService_, _$state_, _$rootScope_, _sweet_,
      _ToastsService_) ->
    $controller = _$controller_
    $state = _$state_
    sweet = _sweet_
    $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
    $rootScope = _$rootScope_
    TenantsService = _TenantsService_
    LocationsService = _LocationsService_
    ToastsService = _ToastsService_
    scope = $rootScope.$new()
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
    }

  describe 'initialization', ->
    controller = undefined

    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      locationsServicePromise = new skykitProvisioning.q.Mock
      controller = $controller 'TenantLocationCtrl', serviceInjection

    it 'should set tenantKey to $stateParams.tenantKey', ->
      expect(controller.tenantKey).toBe $stateParams.tenantKey

    describe 'editing an existing location', ->
      beforeEach ->
        $stateParams = {locationKey: 'fahdsfyudsyfauisdyfoiusydfu'}
        serviceInjection = {
          $scope: scope
          $stateParams: $stateParams
          TenantsService: TenantsService
          LocationsService: LocationsService
        }
        spyOn(TenantsService, 'getTenantByKey').and.returnValue tenantsServicePromise
        spyOn(LocationsService, 'getLocationByKey').and.returnValue locationsServicePromise
        controller = $controller 'TenantLocationCtrl', serviceInjection

      it 'should set editMode to true', ->
        expect(controller.editMode).toBeTruthy()

      it 'should call LocationsService.getLocationByKey', ->
        expect(LocationsService.getLocationByKey).toHaveBeenCalledWith $stateParams.locationKey

    describe '.initialize', ->
      beforeEach ->
        serviceInjection = {
          $scope: scope
          $stateParams: $stateParams
          LocationsService: LocationsService
        }
        controller = $controller 'TenantLocationCtrl', serviceInjection
        controller.initialize()

  describe '.onClickSaveButton', ->
    controller = undefined
    progressBarService = {
      start: ->
      complete: ->
    }
    beforeEach ->
      locationServicePromise = new skykitProvisioning.q.Mock
      spyOn(LocationsService, 'save').and.returnValue locationServicePromise
      spyOn(progressBarService, 'start')
      spyOn(progressBarService, 'complete')
      serviceInjection = {
        ProgressBarService: progressBarService
        LocationsService: LocationsService
        ToastsService: ToastsService
      }
      controller = $controller 'TenantLocationCtrl', serviceInjection
      controller.location = {}
      controller.onClickSaveButton()

    it 'starts the progress bar animation', ->
      expect(progressBarService.start).toHaveBeenCalled()

    it 'call LocationsService.save, pass the current tenant', ->
      expect(LocationsService.save).toHaveBeenCalledWith controller.location

    describe '.onSuccessSavingLocation', ->
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.onSuccessSavingLocation()

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "displays a success toast", ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith 'We saved your location.'

    describe '.onSuccessUpdatingLocation', ->
      tenant_key = 'some key'
      beforeEach ->
        spyOn(ToastsService, 'showSuccessToast')
        controller.editMode = true
        controller.onSuccessUpdatingLocation tenant_key

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "displays a success toast", ->
        expect(ToastsService.showSuccessToast).toHaveBeenCalledWith 'We updated your location.'

    describe '.onFailureSavingLocation 409 conflict', ->
      beforeEach ->
        spyOn(ToastsService, 'showErrorToast')
        spyOn(sweet, 'show')
        errorObject = {status: 409}
        controller.onFailureSavingLocation errorObject

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it 'displays an error toast', ->
        error = 'Location code conflict. Unable to save your location.'
        expect(ToastsService.showErrorToast).toHaveBeenCalledWith error

      it "shows an error alert", ->
        expectedError =
          'Please change your customer location name. Location name must generate a unique location code.'
        expect(sweet.show).toHaveBeenCalledWith 'Oops...', expectedError, 'error'

    describe '.onFailureSavingLocation general error', ->
      beforeEach ->
        spyOn(ToastsService, 'showErrorToast')
        errorObject = {status: 400}
        controller.onFailureSavingLocation errorObject

      it 'stops the progress bar animation', ->
        expect(progressBarService.complete).toHaveBeenCalled()

      it "display error toast", ->
        expectedError = 'Unable to save your location.'
        expect(ToastsService.showErrorToast).toHaveBeenCalledWith expectedError

  describe '.autoGenerateCustomerLocationCode', ->
    beforeEach ->
      controller = $controller 'TenantLocationCtrl', serviceInjection

    it 'generates a new customer location code when key is undefined', ->
      controller.location.key = undefined
      controller.location.customerLocationName = 'Back of Store'
      controller.autoGenerateCustomerLocationCode()
      expect(controller.location.customerLocationCode).toBe 'back_of_store'

    it 'skips generating a new customer location code when key is defined', ->
      controller.location.key = 'd8ad97ad87afg897f987g0f8'
      controller.location.customerLocationName = 'Foobar Inc.'
      controller.location.customerLocationCode = 'back_of_store'
      controller.autoGenerateCustomerLocationCode()
      expect(controller.location.customerLocationCode).toBe 'back_of_store'

