'use strict'

describe 'ProofPlayService', ->
  ProofPlayService = undefined
  $http = undefined
  $httpBackend = undefined
  q = undefined
  window = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$httpBackend_, _$q_, _ProofPlayService_, _$http_, _$window_) ->
    ProofPlayService = _ProofPlayService_
    $http = _$http_
    $httpBackend = _$httpBackend_
    q = _$q_
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


    it 'downloads single-resource csv across date range', ->
      start_date = 12312
      end_date = 234234
      resource = "some_resource"
      ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByDate(start_date, end_date, resource)
      expect(window.open).toHaveBeenCalled()
      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/one_resource_by_date/' + start_date + '/' + end_date + '/' + resource, '_blank')



    it 'downloads single-resource csv across date range by location', ->
      start_date = 12312
      end_date = 234234
      resource = "some_resource"
      ProofPlayService.downloadCSVForSingleResourceAcrossDateRangeByLocation(start_date, end_date, resource)
      expect(window.open).toHaveBeenCalled()
      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/one_resource_by_device/' + start_date + '/' + end_date + '/' + resource, '_blank')

    it 'downloads multi-resource csv across date range', ->
      start_date = 12312
      end_date = 234234
      resources = ["some_resource", "another"]
      ProofPlayService.downloadCSVForMultipleResources(start_date, end_date, resources)
      expect(window.open).toHaveBeenCalled()

      allResources = []

      for each in resources
        allResources = allResources + "-" + each

      expect(window.open).toHaveBeenCalledWith('proofplay/api/v1/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources, '_blank')


  describe 'querySearch filters array by text', ->

    it 'filters properly', ->
      resources = ["some_resource", "other", "again", "otherwise"]
      new_resources = ProofPlayService.querySearch resources, 'oth'
      expect(angular.equals(["other", "otherwise"], new_resources)).toBeTruthy()
      other_new_resources = ProofPlayService.querySearch resources
      expect(angular.equals(other_new_resources, resources)).toBeTruthy()

