'use strict'

describe 'ProofOfPlayOneResourceCtrl', ->
  $controller = undefined
  controller = undefined
  ProofPlayService = undefined
  promise = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _ProofPlayService_) ->
    $controller = _$controller_
    ProofPlayService = _ProofPlayService_
    controller = $controller 'ProofOfPlayOneResourceCtrl', {ProofPlayService: ProofPlayService}

  describe 'initialization', ->
    it 'radioButtonChoices should equal', ->
      radioButtonChoices = {
        group1: 'By Location',
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
        resource: false,
        type: false
      }
      expect(angular.equals(formValidity, controller.formValidity)).toBeTruthy()

    it 'config objects should equal', ->
      expect(controller.no_cache).toBeTruthy()
      expect(controller.loading).toBeTruthy()
      expect(controller.disabled).toBeTruthy()


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
      spyOn(ProofPlayService, 'downloadCSVForSingleResourceAcrossDateRangeByLocation').and.returnValue true
      spyOn(ProofPlayService, 'downloadCSVForSingleResourceAcrossDateRangeByDate').and.returnValue true


    it 'call getAllResources to populate autocomplete with resources', ->
      controller.initialize()
      expect(ProofPlayService.getAllResources).toHaveBeenCalled()


    it 'call querySearch accesses service', ->
      controller.initialize()
      controller.querySearch(resourcesData.data.resources, "one")
      expect(ProofPlayService.querySearch).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved resources data in the controller and loading to be done", ->
      controller.initialize()
      promise.resolve resourcesData
      expect(controller.resources).toBe resourcesData.data.resources
      expect(controller.loading).toBeFalsy()

    it "isRadioValid function sets formValidity type", ->
      controller.isRadioValid("test")
      expect(controller.formValidity.type).toBe "test"

    it 'isStartDateValid sets formValidity start_date', ->
      someDate = new Date()
      controller.isStartDateValid(someDate)
      expect(controller.formValidity.start_date).toBe true

    it 'isEndDateValid sets formValidity end_date', ->
      someDate = new Date()
      controller.isEndDateValid(someDate)
      expect(controller.formValidity.end_date).toBe true


    it 'isResourceValid sets formValidity resource', ->
      controller.initialize()
      promise.resolve resourcesData
      some_resource = resourcesData.data.resources[1]
      controller.isResourceValid(some_resource)
      expect(controller.formValidity.resource).toBe some_resource

      bad_resource = "this is not in the resources array"
      controller.isResourceValid(bad_resource)
      expect(controller.formValidity.resource).toBe null

    it 'disabled is false if formValidity keys are true', ->
      controller.initialize()
      controller.formValidity.start_date = true
      controller.formValidity.end_date = true
      controller.formValidity.resource = true
      controller.formValidity.type = true
      controller.isDisabled()
      expect(controller.disabled).toBeFalsy()


    it 'submission hits ProofPlayService download CSV based on type', ->
      controller.initialize()
      controller.formValidity.start_date = true
      controller.formValidity.end_date = true
      controller.formValidity.resource = true
      controller.formValidity.type = true
      controller.isDisabled()
      controller.final = {
        start_date_unix: moment(new Date()).unix(),
        end_date_unix: moment(new Date()).unix(),
        resource: resourcesData.data.resources[0],
        type: "1"
      }
      controller.submit()
      expect(ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByLocation).toHaveBeenCalled()

      controller.final.type = "2"
      controller.submit()
      expect(ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByDate).toHaveBeenCalled()
