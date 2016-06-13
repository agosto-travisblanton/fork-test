'use strict'

describe 'ProofPlayService', ->
  ProofPlayService = undefined
  $http = undefined
  $stateParams = undefined
  $state = undefined
  ToastsService = undefined
  Lockr = undefined
  deferred = undefined
  $q = undefined
  promise = undefined
  $rootScope = undefined
  window = undefined
  StorageService = undefined
  cookie_token = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$httpBackend_, _$q_, _ProofPlayService_, _$http_, _$window_, _StorageService_, _ToastsService_, _$state_) ->
    ProofPlayService = _ProofPlayService_
    $http = _$http_
    ToastsService = _ToastsService_
    $httpBackend = _$httpBackend_
    $q = _$q_
    $stateParams = {}
    $state = _$state_
    StorageService = _StorageService_
    window = _$window_


  describe 'querying for csvs', ->
    beforeEach ->
      spyOn(window, 'open').and.callFake(() ->
        return true
      )
      promise = new skykitProvisioning.q.Mock
      spyOn($state, 'go')
      spyOn($q, 'defer')
      deferred = $q.defer()
      spyOn(ToastsService, 'showErrorToast')
      spyOn(ToastsService, 'showSuccessToast')
      cookie_token = 'test'
      StorageService.set('currentDistributorKey', cookie_token)


    it 'sets @uriBase variable', ->
      expect(ProofPlayService.uriBase).toEqual 'proofplay/api/v1'

    it 'sets @cachedResources variable to null', ->
      expect(ProofPlayService.cachedResources).toBeFalsy()

    it 'sets tenant and downloads multi-resource csv across date range', ->
      start_date = 12312
      end_date = 234234
      resources = ["some_resource", "another"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.downloadCSVForMultipleResourcesByDate(start_date, end_date, resources, tenants[0])
      expect(window.open).toHaveBeenCalled()

      allResources = []

      for each in resources
        allResources = allResources + "|" + each

      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources + "/" + tenants[0] + "/" + cookie_token, '_blank')


    it 'sets tenant and downloadCSVForMultipleResourcesByDevice', ->
      start_date = 12312
      end_date = 234234
      resources = ["some_resource", "another"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.downloadCSVForMultipleResourcesByDevice(start_date, end_date, resources, tenants[0])
      expect(window.open).toHaveBeenCalled()

      allResources = ''

      for each in resources
        allResources = allResources + "|" + each


      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_resource_by_device/' + start_date + '/' + end_date + '/' + allResources + "/" + tenants[0] + "/" + cookie_token, '_blank')


    it 'sets tenant and downloads multi-devices summarized csv', ->
      start_date = 12312
      end_date = 234234
      devices = ["some_devices", "another_device"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.downloadCSVForMultipleDevicesSummarized(start_date, end_date, devices, tenants[0])
      expect(window.open).toHaveBeenCalled()

      allDevices = ''

      for each in devices
        allDevices = allDevices + "|" + each


      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_device_summarized/' + start_date + '/' + end_date + '/' + allDevices + "/" + tenants[0] + "/" + cookie_token, '_blank')

    it 'sets tenant and downloadCSVForMultipleDevicesByDate', ->
      start_date = 12312
      end_date = 234234
      devices = ["some_devices", "another_device"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.downloadCSVForMultipleDevicesByDate(start_date, end_date, devices, tenants[0])
      expect(window.open).toHaveBeenCalled()

      allDevices = ''

      for each in devices
        allDevices = allDevices + "|" + each


      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_device_by_date/' + start_date + '/' + end_date + '/' + allDevices + "/" + tenants[0] + "/" + cookie_token, '_blank')

    it 'sets tenant and downloadCSVForMultipleLocationsByDevice', ->
      start_date = 12312
      end_date = 234234
      locations = ["some_location", "another_location"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.downloadCSVForMultipleLocationsByDevice(start_date, end_date, locations, tenants[0])
      expect(window.open).toHaveBeenCalled()

      allLocations = ''

      for each in locations
        allLocations = allLocations + "|" + each


      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_location_by_device/' + start_date + '/' + end_date + '/' + allLocations + "/" + tenants[0] + "/" + cookie_token, '_blank')


    it 'sets tenant and downloadCSVForMultipleLocationsSummarized', ->
      start_date = 12312
      end_date = 234234
      locations = ["some_location", "another_location"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.downloadCSVForMultipleLocationsSummarized(start_date, end_date, locations, tenants[0])
      expect(window.open).toHaveBeenCalled()

      allLocations = ''

      for each in locations
        allLocations = allLocations + "|" + each

      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_location_summarized/' + start_date + '/' + end_date + '/' + allLocations + "/" + tenants[0] + "/" + cookie_token, '_blank')

      it 'gets all tenants', ->
        to_respond = {
          data: {
            tenants: ["one", "two"]
          }
        }
        $httpBackend.expectGET("proofplay/api/v1/retrieve_my_tenants").respond(to_respond)
        ProofPlayService.getAllTenants()
        .then (data) ->
          expect(angular.equals(data.data.tenants, to_respond.data.tenants))
  
        $httpBackend.flush()


      it 'gets all displays of a tenant', ->
        to_respond = {
          data: {
            displays: ["one", "two"]
          }
        }
  
        chosen_tenant = "some-tenant"
        $httpBackend.expectGET("proofplay/api/v1/retrieve_all_displays/" + chosen_tenant).respond(to_respond)
  
        ProofPlayService.getAllDisplays(chosen_tenant)
        .then (data) ->
          expect(angular.equals(data.data.displays, to_respond.data.displays))
  
        $httpBackend.flush()

      it 'gets all locations of a tenant', ->
        to_respond = {
          data: {
            locations: ["one", "two"]
          }
        }
  
        chosen_tenant = "some-tenant"
  
        $httpBackend.expectGET("proofplay/api/v1/retrieve_all_locations/" + chosen_tenant).respond(to_respond)
  
        ProofPlayService.getAllLocations(chosen_tenant)
        .then (data) ->
          expect(angular.equals(data.data.locations, to_respond.data.locations))
  
        $httpBackend.flush()


  describe 'querySearch filters array by text', ->
    it 'filters properly', ->
      resources = ["some_resource", "other", "again", "otherwise"]
      new_resources = ProofPlayService.querySearch resources, 'oth'
      expect(angular.equals(["other", "otherwise"], new_resources)).toBeTruthy()
      other_new_resources = ProofPlayService.querySearch resources
      expect(angular.equals(other_new_resources, resources)).toBeTruthy()

