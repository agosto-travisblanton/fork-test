'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'DevicesService', ($http, $log, Restangular) ->
  class DevicesService
    SERVICE_NAME = 'devices'
    @uriBase = 'v1/devices'

    getDeviceByMacAddress: (macAddress) ->
      Restangular.oneUrl('api/v1/devices', "api/v1/devices?mac_address=#{macAddress}").get()

    getDeviceByKey: (deviceKey) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{deviceKey}").get()
      promise

    getDevicesByTenant: (tenantKey) ->
      unless tenantKey == undefined
        promise = Restangular.one('tenants', tenantKey).doGET(SERVICE_NAME)
        promise

    getDevicesByDistributor: (distributorKey) ->
      unless distributorKey == undefined
        promise = Restangular.one('distributors', distributorKey).doGET(SERVICE_NAME)
        promise

    getDevices: ->
      promise = Restangular.all(SERVICE_NAME).getList()
      promise

    save: (device) ->
      if device.key != undefined
        promise = device.put()
      else
        promise = Restangular.service('devices').post(device)
      promise

    getPanelModels: () ->
      [
        {
          'id': 'None'
          'displayName': 'None'
        }
        {
          'id': 'Sony-FXD40LX2F'
          'displayName': 'Sony FXD40LX2F'
        }
        {
          'id': 'NEC-LCD4215'
          'displayName': 'NEC LCD4215'
        }
        {
          'id': 'Phillips-BDL5560EL'
          'displayName': 'Phillips BDL5560EL'
        }
        {
          'id': 'Panasonic-TH55LF6U'
          'displayName': 'Panasonic TH55LF6U'
        }
        {
          'id': 'Sharp-PNE521'
          'displayName': 'Sharp PNE521'
        }
      ]

    getPanelInputs: () ->
      [
        {
          'id': '0'
          'displayName': 'None'
          'parentId': 'None'
        }
        {
          'id': 'son1'
          'displayName': 'HDMI1'
          'parentId': 'Sony-FXD40LX2F'
        }
        {
          'id': 'son2'
          'displayName': 'HDMI2'
          'parentId': 'Sony-FXD40LX2F'
        }
        {
          'id': 'phi1'
          'displayName': 'HDMI1'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'phi2'
          'displayName': 'HDMI2'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'phi3'
          'displayName': 'DVI'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'pan1'
          'displayName': 'HDMI1'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'pan2'
          'displayName': 'HDMI2'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'pan3'
          'displayName': 'DVI'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'sha1'
          'displayName': 'HDMI1'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha2'
          'displayName': 'HDMI2'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha3'
          'displayName': 'DVI'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'nec1'
          'displayName': 'TBD'
          'parentId': 'NEC-LCD4215'
        }
      ]

  new DevicesService()
