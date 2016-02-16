'use strict'

describe 'ProofOfPlayMultiResourceCtrl', ->
  $controller = undefined
  controller = undefined
  ProofPlayService = undefined
  promise = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _ProofPlayService_) ->
    $controller = _$controller_
    ProofPlayService = _ProofPlayService_
    controller = $controller 'ProofOfPlayMultiResourceCtrl', {ProofPlayService: ProofPlayService}

  describe 'initialization', ->
    it 'radioButtonChoices should equal', ->
      radioButtonChoices = {
        group1: 'By Device',
        group2: 'By Date',
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
        resources: false,
      }
      expect(angular.equals(formValidity, controller.formValidity)).toBeTruthy()

    it 'config objects should equal', ->
      expect(controller.no_cache).toBeTruthy()
      expect(controller.loading).toBeTruthy()
      expect(controller.disabled).toBeTruthy()
      expect(angular.isArray(controller.selected_resources)).toBeTruthy()


  describe '.initialize', ->
    resourcesData = {
      data: {
        resources: ["one resource", "two resource", "three resource", "four"]
      }
    }

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      querySearch = () ->
      spyOn(ProofPlayService, 'getAllResources').and.returnValue promise
      spyOn(ProofPlayService, 'querySearch').and.returnValue querySearch
      spyOn(ProofPlayService, 'downloadCSVForMultipleResourcesByDate').and.returnValue true
      spyOn(ProofPlayService, 'downloadCSVForMultipleResourcesByDevice').and.returnValue true


    it 'call getAllResources to populate autocomplete with resources', ->
      controller.initialize()
      expect(ProofPlayService.getAllResources).toHaveBeenCalled()


    it 'call querySearch accesses service', ->
      controller.initialize()
      controller.querySearch(resourcesData.data.resources, "one")
      expect(ProofPlayService.querySearch).toHaveBeenCalled()

    it "isRadioValid function sets formValidity type", ->
      controller.isRadioValid("test")
      expect(controller.formValidity.type).toBe "test"

    it "the 'then' handler caches the retrieved resources data in the controller and loading to be done", ->
      controller.initialize()
      promise.resolve resourcesData
      expect(controller.resources).toBe resourcesData.data.resources
      expect(controller.loading).toBeFalsy()


    it 'isStartDateValid sets formValidity start_date', ->
      someDate = new Date()
      controller.isStartDateValid(someDate)
      expect(controller.formValidity.start_date).toBe true

    it 'isEndDateValid sets formValidity end_date', ->
      someDate = new Date()
      controller.isEndDateValid(someDate)
      expect(controller.formValidity.end_date).toBe true


    it 'isResourceValid returns validity', ->
      controller.initialize()
      promise.resolve resourcesData

      controller.selected_resources = [resourcesData.data.resources[0]]
      resourceValidity = controller.isResourceValid(resourcesData.data.resources[0])
      expect(resourceValidity).toBeFalsy()
      controller.selected_resources = []
      newResourceValidity = controller.isResourceValid(resourcesData.data.resources[0])
      expect(newResourceValidity).toBeTruthy()
      newResourceValidity = controller.isResourceValid("something not in resources")
      expect(newResourceValidity).toBeFalsy()


    it 'areResourcesValid sets formValidity resources value', ->
      controller.selected_resources = ["at least one value here"]
      controller.areResourcesValid()
      expect(controller.formValidity.resources).toBeTruthy()

    it 'disabled is false if formValidity keys are true', ->
      controller.formValidity.start_date = true
      controller.formValidity.end_date = true
      controller.formValidity.resources = true
      controller.formValidity.type = true
      controller.isDisabled()
      expect(controller.disabled).toBeFalsy()


    it 'adds to selected resource if resource is valid', ->
      controller.initialize()
      promise.resolve resourcesData
      controller.addToSelectedResources(resourcesData.data.resources[0])
      expect(angular.equals(controller.resources, ["two resource", "three resource", "four"])).toBeTruthy()
      expect(angular.equals(controller.selected_resources, ['one resource'])).toBeTruthy()


    it 'removes from selected resource', ->
      controller.initialize()
      promise.resolve resourcesData
      controller.addToSelectedResources(resourcesData.data.resources[0])
      controller.removeFromSelectedResource(resourcesData.data.resources[0])
      expect(controller.selected_resources.length).toEqual(0)


    it 'opens window when submit gets called', ->
      controller.final = {
        start_date_unix: moment(new Date()).unix(),
        end_date_unix: moment(new Date()).unix(),
        resources: ["some", "resources"],
        type: "1"
      }
      controller.submit()
      expect(ProofPlayService.downloadCSVForMultipleResourcesByDevice).toHaveBeenCalled()

      controller.final.type = "2"
      controller.submit()
      expect(ProofPlayService.downloadCSVForMultipleResourcesByDate).toHaveBeenCalled()
