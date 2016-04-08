'use strict'

angular.module('skykitProvisioning')
.factory 'ProofPlayService', ($http, $q, $window, $cookies) ->
  new class ProofPlayService

    constructor: ->
      @uriBase = 'proofplay/api/v1'
      @cachedResources = null
      @chosenTenant = null


    setTenant: (tenant) ->
      @chosenTenant = tenant
      
    getTenant: () ->
      return @chosenTenant


    createFilterFor: (query) ->
      query = angular.lowercase(query)
      (resource) ->
        resource = angular.lowercase(resource)
        return (resource.indexOf(query) == 0)


    getAllResources: () ->
      deferred = $q.defer()
      if @cachedResources
        deferred.
        resolve(@cachedResources)
      else
        distributorKey = $cookies.get('currentDistributorKey')
        $http.get(@uriBase + '/retrieve_all_resources/' + @chosenTenant,
          headers: {
            'X-Provisioning-Distributor': distributorKey
          }
        )
        .then (data) =>
          @cachedResource = data
          deferred.resolve(data)

      deferred.promise


    getAllDisplays: () ->
      distributorKey = $cookies.get('currentDistributorKey')
      $http.get(@uriBase + '/retrieve_all_displays/' + @chosenTenant,
        headers: {
          'X-Provisioning-Distributor': distributorKey
        }
      )

    getAllLocations: () ->
      distributorKey = $cookies.get('currentDistributorKey')
      $http.get(@uriBase + '/retrieve_all_locations/' + @chosenTenant,
        headers: {
          'X-Provisioning-Distributor': distributorKey
        }
      )


    getAllTenants: () ->
      distributorKey = $cookies.get('currentDistributorKey')
      $http.get(@uriBase + '/retrieve_my_tenants',
        headers: {
          'X-Provisioning-Distributor': distributorKey
        }
      )


    downloadCSVForMultipleResourcesByDate: (start_date, end_date, resources) ->
      allResources = ''

      for each in resources
        allResources = allResources + "|" + each

      $window.open(@uriBase + '/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources + '/' +
          @chosenTenant + "/" + $cookies.get('currentDistributorKey')

      , '_blank')
      return true


    downloadCSVForMultipleResourcesByDevice: (start_date, end_date, resources) ->
      allResources = ''

      for each in resources
        allResources = allResources + "|" + each

      $window.open(@uriBase + '/multi_resource_by_device/' + start_date + '/' + end_date + '/' + allResources + '/' +
          @chosenTenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true



    downloadCSVForMultipleDevicesSummarized: (start_date, end_date, devices) ->
      allDevices = ''

      for each in devices
        allDevices = allDevices + "|" + each

      $window.open(@uriBase + '/multi_device_summarized/' + start_date + '/' + end_date + '/' + allDevices + '/' +
          @chosenTenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true


    downloadCSVForMultipleDevicesByDate: (start_date, end_date, devices) ->
      allDevices = ''

      for each in devices
        allDevices = allDevices + "|" + each

      $window.open(@uriBase + '/multi_device_by_date/' + start_date + '/' + end_date + '/' + allDevices + '/' +
          @chosenTenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true

    downloadCSVForMultipleLocationsByDevice: (start_date, end_date, locations) ->
      allLocations = ''

      for each in locations
        allLocations = allLocations + "|" + each

      $window.open(@uriBase + '/multi_location_by_device/' + start_date + '/' + end_date + '/' + allLocations + '/' +
          @chosenTenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true

    downloadCSVForMultipleLocationsSummarized: (start_date, end_date, locations) ->
      allLocations = ''

      for each in locations
        allLocations = allLocations + "|" + each

      $window.open(@uriBase + '/multi_location_summarized/' + start_date + '/' + end_date + '/' + allLocations + '/' +
          @chosenTenant + "/" + $cookies.get('currentDistributorKey')
      , '_blank')
      return true


    querySearch: (resources, searchText) ->
      if searchText
        resources.filter(this.createFilterFor(searchText))
      else
        resources
