'use strict'

angular.module('skykitProvisioning')
.factory 'ProofPlayService', ($http) ->
  new class ProofPlayService

    constructor: ->
      @uriBase = '/api/v1/proofplay'

    getAllResources: () ->
      $http.get(@uriBase + '/retrieve_all_resources')

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