'use strict'

describe 'ProofOfPlayMultiLocationCtrl', ->
  $controller = undefined
  controller = undefined
  ProofPlayService = undefined
  $stateParams = undefined
  $state = undefined
  ToastsService = undefined
  promise = undefined
  selected_tenant = undefined

  beforeEach module('skykitProvisioning')
  
  beforeEach inject (_$controller_, _ProofPlayService_, _ToastsService_, _$state_) ->
    $controller = _$controller_
    ProofPlayService = _ProofPlayService_
    ToastsService = _ToastsService_
    $stateParams = {}
    $state = _$state_
    controller = $controller 'ProofOfPlayMultiLocationCtrl', {
      ProofPlayService: ProofPlayService,
      ToastsService: ToastsService,
      $stateParams: $stateParams,
      $state: $state
    }

  describe 'initialization', ->
    it 'radioButtonChoices should equal', ->
      radioButtonChoices = {
        group1: 'By Device',
        group2: 'Summarized',
        selection: null
      }
      expect(angular.equals(radioButtonChoices, controller.radioButtonChoices)).toBeTruthy()

    it 'dateTimeSelection should equal', ->
      dateTimeSelection = {
        start: null,
        end: null
      }
      expect(angular.equals(dateTimeSelection, controller.dateTimeSelection)).toBeTruthy()


    it 'dateTimeSelection should equal', ->
      formValidity = {
        start_date: false,
        end_date: false,
        locations: false,
      }
      expect(angular.equals(formValidity, controller.formValidity)).toBeTruthy()

    it 'config objects should equal', ->
      expect(controller.no_cache).toBeTruthy()
      expect(controller.loading).toBeTruthy()
      expect(controller.disabled).toBeTruthy()
      expect(angular.isArray(controller.selected_locations)).toBeTruthy()


  describe '.initialize', ->
    locationsData = {
      data: {
        locations: ["one resource", "two resource", "three resource", "four"]
      }
    }

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      querySearch = () ->
      spyOn($state, 'go')
      spyOn(ProofPlayService, 'getAllLocations').and.returnValue promise
      spyOn(ProofPlayService, 'querySearch').and.returnValue querySearch
      spyOn(ProofPlayService, 'downloadCSVForMultipleLocationsByDevice').and.returnValue true
      spyOn(ProofPlayService, 'downloadCSVForMultipleLocationsSummarized').and.returnValue true


    it 'call getAllLocations to populate autocomplete with locations', ->
      controller.initialize()
      promise.resolve locationsData
      expect(ProofPlayService.getAllLocations).toHaveBeenCalled()


    it 'call querySearch accesses service', ->
      controller.initialize()
      controller.querySearch(locationsData.data.locations, "one")
      expect(ProofPlayService.querySearch).toHaveBeenCalled()

    it "isRadioValid function sets formValidity type", ->
      controller.isRadioValid("test")
      expect(controller.formValidity.type).toBe "test"

    it "the 'then' handler caches the retrieved locations data in the controller and loading to be done", ->
      controller.initialize()
      promise.resolve locationsData
      expect(controller.locations).toBe locationsData.data.locations
      expect(controller.loading).toBeFalsy()


    it 'isStartDateValid sets formValidity start_date', ->
      someDate = new Date()
      controller.isStartDateValid(someDate)
      expect(controller.formValidity.start_date).toBe true

    it 'isEndDateValid sets formValidity end_date', ->
      someDate = new Date()
      controller.isEndDateValid(someDate)
      expect(controller.formValidity.end_date).toBe true


    it 'isLocationValid returns validity', ->
      controller.initialize()
      promise.resolve locationsData

      controller.selected_locations = [locationsData.data.locations[0]]
      resourceValidity = controller.isLocationValid(locationsData.data.locations[0])
      expect(resourceValidity).toBeFalsy()
      controller.selected_locations = []
      newResourceValidity = controller.isLocationValid(locationsData.data.locations[0])
      expect(newResourceValidity).toBeTruthy()
      newResourceValidity = controller.isLocationValid("something not in locations")
      expect(newResourceValidity).toBeFalsy()


    it 'areLocationsValid sets formValidity locations value', ->
      controller.selected_locations = ["at least one value here"]
      controller.areLocationsValid()
      expect(controller.formValidity.locations).toBeTruthy()

    it 'disabled is false if formValidity keys are true', ->
      controller.formValidity.start_date = true
      controller.formValidity.end_date = true
      controller.formValidity.locations = true
      controller.formValidity.type = true
      controller.isDisabled()
      expect(controller.disabled).toBeFalsy()


    it 'adds to selected resource if resource is valid', ->
      controller.initialize()
      promise.resolve locationsData
      controller.addToSelectedLocations(locationsData.data.locations[0])
      expect(angular.equals(controller.locations, ["two resource", "three resource", "four"])).toBeTruthy()
      expect(angular.equals(controller.selected_locations, ['one resource'])).toBeTruthy()


    it 'removes from selected resource', ->
      controller.initialize()
      promise.resolve locationsData
      controller.addToSelectedLocations(locationsData.data.locations[0])
      controller.removeFromSelectedLocation(locationsData.data.locations[0])
      expect(controller.selected_locations.length).toEqual(0)


    it 'opens window when submit gets called', ->
      controller.final = {
        start_date_unix: moment(new Date()).unix(),
        end_date_unix: moment(new Date()).unix(),
        locations: ["some", "locations"],
        type: "1"
      }
      controller.submit()
      expect(ProofPlayService.downloadCSVForMultipleLocationsByDevice).toHaveBeenCalled()

      controller.final.type = "2"
      controller.submit()
      expect(ProofPlayService.downloadCSVForMultipleLocationsSummarized).toHaveBeenCalled()

  describe '.tenant change related functions', ->
    
    selected_tenant = "some_tenant"
    
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn($state, 'go')
      spyOn(ProofPlayService, 'getAllLocations').and.returnValue promise
      spyOn(ProofPlayService, 'getAllTenants').and.returnValue promise


    it 'initializeTenantSelection sets tenants', ->
      controller.initialize_tenant_select()
      to_resolve = {
        data: {
          tenants: ["one", "two"]
        }
      }
      promise.resolve to_resolve
      expect(controller.tenants).toEqual ["one", "two"]


    it 'submitTenants sets currentTenant and getsAllDisplays again', ->
      controller.submitTenant(selected_tenant)
      expect($state.go).toHaveBeenCalledWith 'proofDetail', {tenant: selected_tenant}
