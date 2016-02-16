'use strict'

angular.module('skykitProvisioning')
.factory 'ProofPlayService', ($http, $q, $window) ->
  new class ProofPlayService

    constructor: ->
      @uriBase = 'proofplay/api/v1'
      @cachedResources = null

    createFilterFor: (query) ->
      query = angular.lowercase(query)
      (resource) ->
        resource = angular.lowercase(resource)
        return (resource.indexOf(query) == 0)

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
      $window.open(@uriBase + '/one_resource_by_date/' + start_date + '/' + end_date + '/' + resource, '_blank')
      return true

    downloadCSVForSingleResourceAcrossDateRangeByLocation: (start_date, end_date, resource) ->
      $window.open(@uriBase + '/one_resource_by_device/' + start_date + '/' + end_date + '/' + resource, '_blank')
      return true

    downloadCSVForMultipleResources: (start_date, end_date, resources) ->
      allResources = []

      for each in resources
        allResources = allResources + "-" + each

      $window.open(@uriBase + '/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources, '_blank')
      return true

    querySearch: (resources, searchText) ->
      if searchText
        resources.filter(this.createFilterFor(searchText))
      else
        resources
