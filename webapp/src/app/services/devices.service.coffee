'use strict'

angular.module('skykitProvisioning').factory 'DevicesService', ($http, $log, Restangular) ->
  class DevicesService
    SERVICE_NAME = 'devices'
    @uriBase = 'v1/devices'

    getDeviceByMacAddress: (macAddress) ->
      Restangular.oneUrl('api/v1/devices', "api/v1/devices?mac_address=#{macAddress}").get()

    getDeviceByKey: (deviceKey) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/devices/#{deviceKey}").get()
      promise

    getIssuesByKey: (deviceKey, startEpoch, endEpoch) ->
      promise = Restangular.oneUrl(SERVICE_NAME,
        "api/v1/devices/#{deviceKey}/issues?start=#{startEpoch}&end=#{endEpoch}").get()
      promise

    getCommandEventsByKey: (deviceKey) ->
      promise = Restangular.oneUrl(SERVICE_NAME,
        "/api/v1/player-command-events/#{deviceKey}").get()
      promise

    getDevicesByTenant: (tenantKey) ->
      unless tenantKey == undefined
        url = "api/v1/tenants/#{tenantKey}/devices?unmanaged=false"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    getUnmanagedDevicesByTenant: (tenantKey) ->
      unless tenantKey == undefined
        url = "api/v1/tenants/#{tenantKey}/devices?unmanaged=true"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    getDevicesByDistributor: (distributorKey) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/#{distributorKey}/devices?unmanaged=false"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    getUnmanagedDevicesByDistributor: (distributorKey) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/#{distributorKey}/devices?unmanaged=true"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
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
          'id': 'None'
          'parentId': 'None'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Sony-FXD40LX2F'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Sony-FXD40LX2F'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'DVI'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'DVI'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'DVI'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'VGA'
          'parentId': 'NEC-LCD4215'
        }
        {
          'id': 'DVI1'
          'parentId': 'NEC-LCD4215'
        }
      ]

  new DevicesService()
