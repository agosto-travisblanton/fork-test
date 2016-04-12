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

    searchDevicesByPartialSerial: (distributorKey, partial_serial, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/search/serial/#{distributorKey}/#{partial_serial}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    searchDevicesByPartialMac: (distributorKey, partial_mac, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/search/mac/#{distributorKey}/#{partial_mac}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    matchDevicesByFullSerial: (distributorKey, full_serial, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/match/serial/#{distributorKey}/#{full_serial}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    matchDevicesByFullMac: (distributorKey, full_mac, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/match/mac/#{distributorKey}/#{full_mac}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    getDevicesByDistributor: (distributorKey, prev, next) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/#{prev}/#{next}/#{distributorKey}/devices?unmanaged=false"
        promise = Restangular.oneUrl(SERVICE_NAME, url).get()
        promise

    getUnmanagedDevicesByDistributor: (distributorKey, prev, next) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/#{prev}/#{next}/#{distributorKey}/devices?unmanaged=true"
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

    delete: (deviceKey) ->
      promise = Restangular.one(SERVICE_NAME, deviceKey).remove()
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
