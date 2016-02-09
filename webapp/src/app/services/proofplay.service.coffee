'use strict'

angular.module('skykitProvisioning')
.factory 'ProofPlayService', ($http, $q) ->
  new class ProofPlayService

    constructor: ->
      @uriBase = 'proofplay/api/v1'
      @cachedResources = null

    getAllResources: () ->
      deferred = $q.defer()
      if @cachedResources
        deferred.resolve(@cachedResources)
      else
        $http.get(@uriBase + '/retrieve_all_resources')
        .then (data) =>
          @cachedResource = data
          deferred.resolve(data)
      deferred.promise


    downloadCSVForSingleResourceAcrossDateRangeByDate: (start_date, end_date, resource) ->
      window.open(@uriBase + '/one_resource_by_date/' + start_date + '/' + end_date + '/' + resource, '_blank')


    downloadCSVForSingleResourceAcrossDateRangeByLocation: (start_date, end_date, resource) ->
      window.open(@uriBase + '/one_resource_by_device/' + start_date + '/' + end_date + '/' + resource, '_blank')

    downloadCSVForMultipleResources: (start_date, end_date, resources) ->
      allResources = []

      for each in resources
        allResources = allResources + "-" + item

      window.open(@uriBase + '/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources, '_blank')

    test: () ->
      0