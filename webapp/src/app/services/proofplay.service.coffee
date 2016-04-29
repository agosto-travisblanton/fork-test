'use strict'

angular.module('skykitProvisioning')
.factory 'ProofPlayService', ($http, $q, $window, $cookies, $stateParams, $state, ToastsService) ->
  new class ProofPlayService

    constructor: ->
      @uriBase = 'proofplay/api/v1'

    createFilterFor: (query) ->
      query = angular.lowercase(query)
      (resource) ->
        resource = angular.lowercase(resource)
        return (resource.indexOf(query) == 0)


    makeHTTPRequest: (where_to_go, tenant) =>
      distributorKey = $cookies.get('currentDistributorKey')
      $http.get(@uriBase + where_to_go + tenant,
        headers: {
          'X-Provisioning-Distributor': distributorKey
        }
      )

    getAllResources: (tenant) ->
      r = @makeHTTPRequest("/retrieve_all_resources/", tenant)


      r.catch (err, data) ->
        status = err.status
        if status == 403
          ToastsService.showErrorToast "You are not allowed to view this tenant!"
          $state.go 'proof', {}
        if status == 404
          ToastsService.showErrorToast "You must select a tenant first!"
          $state.go 'proof', {}

      r.then (data) ->
        return data


    getAllDisplays: (tenant) ->
      @makeHTTPRequest("/retrieve_all_displays/", tenant)


    getAllLocations: (tenant) ->
      @makeHTTPRequest("/retrieve_all_locations/", tenant)


    getAllTenants: () ->
      @makeHTTPRequest("/retrieve_my_tenants", '')



    downloadCSVForMultipleResourcesByDate: (start_date, end_date, resources, tenant) ->
      allResources = ''

      for each in resources
        allResources = allResources + "|" + each

      $window.open(@uriBase + '/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources + '/' +
          tenant + "/" + $cookies.get('currentDistributorKey')

      , '_blank')
      return true


    downloadCSVForMultipleResourcesByDevice: (start_date, end_date, resources, tenant) ->
      allResources = ''

      for each in resources
        allResources = allResources + "|" + each

      $window.open(@uriBase + '/multi_resource_by_device/' + start_date + '/' + end_date + '/' + allResources + '/' +
          tenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true



    downloadCSVForMultipleDevicesSummarized: (start_date, end_date, devices, tenant) ->
      allDevices = ''

      for each in devices
        allDevices = allDevices + "|" + each

      $window.open(@uriBase + '/multi_device_summarized/' + start_date + '/' + end_date + '/' + allDevices + '/' +
          tenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true


    downloadCSVForMultipleDevicesByDate: (start_date, end_date, devices, tenant) ->
      allDevices = ''

      for each in devices
        allDevices = allDevices + "|" + each

      $window.open(@uriBase + '/multi_device_by_date/' + start_date + '/' + end_date + '/' + allDevices + '/' +
          tenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true

    downloadCSVForMultipleLocationsByDevice: (start_date, end_date, locations, tenant) ->
      allLocations = ''

      for each in locations
        allLocations = allLocations + "|" + each

      $window.open(@uriBase + '/multi_location_by_device/' + start_date + '/' + end_date + '/' + allLocations + '/' +
          tenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true

    downloadCSVForMultipleLocationsSummarized: (start_date, end_date, locations, tenant) ->
      allLocations = ''

      for each in locations
        allLocations = allLocations + "|" + each

      $window.open(@uriBase + '/multi_location_summarized/' + start_date + '/' + end_date + '/' + allLocations + '/' +
          tenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true


    querySearch: (resources, searchText) ->
      if searchText
        resources.filter(this.createFilterFor(searchText))
      else
        resources