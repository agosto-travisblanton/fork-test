'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'DevicesService', ($http, $log, Restangular) ->

  class DevicesService
    @uriBase = 'v1/devices'

    getDeviceByMacAddress: (macAddress) ->
      Restangular.oneUrl('api/v1/devices', "api/v1/devices?mac_address=#{macAddress}").get()

    getDeviceByKey: (deviceKey) ->
      promise = Restangular.oneUrl('devices', "api/v1/devices/#{deviceKey}").get()
      promise

    getDevicesByTenant: (tenantKey) ->
      unless tenantKey == undefined
        promise = Restangular.one('tenants', tenantKey).doGET('devices')
        promise


  new DevicesService()
