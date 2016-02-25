'use strict'

describe 'ProofPlayService', ->
  ProofPlayService = undefined
  $http = undefined
  $httpBackend = undefined
  $cookies = undefined
  q = undefined
  window = undefined
  cookie_token = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$httpBackend_, _$q_, _ProofPlayService_, _$http_, _$window_, _$cookies_) ->
    ProofPlayService = _ProofPlayService_
    $http = _$http_
    $httpBackend = _$httpBackend_
    q = _$q_
    $cookies = _$cookies_
    window = _$window_


  describe 'initialization', ->
    it 'sets @uriBase variable', ->
      expect(ProofPlayService.uriBase).toEqual 'proofplay/api/v1'

    it 'sets @cachedResources variable to null', ->
      expect(ProofPlayService.cachedResources).toBeFalsy()

  describe 'querying for csvs', ->

    beforeEach ->
      spyOn(window, 'open').and.callFake(() ->
        return true
      )
      cookie_token = 'test'
      $cookies.put('currentDistributorKey', cookie_token)


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

    it 'sets tenant and downloads multi-resource csv across date range', ->
      start_date = 12312
      end_date = 234234
      resources = ["some_resource", "another"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.setTenant(tenants[0])
      ProofPlayService.downloadCSVForMultipleResourcesByDate(start_date, end_date, resources)
      expect(window.open).toHaveBeenCalled()

      allResources = []

      for each in resources
        allResources = allResources + "-" + each

      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources + "/" + tenants[0] + "/" + cookie_token, '_blank')


    it 'sets tenant and downloads multi-resource csv across device', ->
      start_date = 12312
      end_date = 234234
      resources = ["some_resource", "another"]
      tenants = ["one_tenant", "two_tenant"]
      ProofPlayService.setTenant(tenants[0])
      ProofPlayService.downloadCSVForMultipleResourcesByDevice(start_date, end_date, resources)
      expect(window.open).toHaveBeenCalled()

      allResources = []

      for each in resources
        allResources = allResources + "-" + each

      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_resource_by_device/' + start_date + '/' + end_date + '/' + allResources + "/" + tenants[0] + "/" + cookie_token, '_blank')



    it 'gets all displays of a tenant', ->
      to_respond = {
        data: {
          displays: ["one", "two"]
        }
      }

      chosen_tenant = "some-tenant"

      ProofPlayService.setTenant(chosen_tenant)

      $httpBackend.expectGET("proofplay/api/v1/retrieve_all_displays/" + chosen_tenant).respond(to_respond)

      ProofPlayService.getAllDisplays()
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

      ProofPlayService.setTenant(chosen_tenant)

      $httpBackend.expectGET("proofplay/api/v1/retrieve_all_locations/" + chosen_tenant).respond(to_respond)

      ProofPlayService.getAllLocations()
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

