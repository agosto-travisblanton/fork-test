'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'DevicesService', ($http, $log, Restangular) ->

  class DevicesService
    @uriBase = 'v1/devices'

    getDeviceByMacAddress: (macAddress) ->
      Restangular.oneUrl('api/v1/devices', "api/v1/devices?mac_address=#{macAddress}").get()

    getDeviceList: () ->
#      Restangular.oneUrl('api/v1/devices', "api/v1/devices").get()

    getDevicesByTenant: (tenant) ->
      if tenant.key != undefined
        promise = Restangular.one('tenants', tenant.key).doGET('devices')
        promise


  new DevicesService()
