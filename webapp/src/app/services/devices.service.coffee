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
          'id': 'Sony–FXD40LX2F'
          'displayName': 'Sony – FXD40LX2F'
        }
        {
          'id': 'NEC–LCD4215'
          'displayName': 'NEC – LCD4215'
        }
        {
          'id': 'Phillips–BDL5560EL'
          'displayName': 'Phillips – BDL5560EL'
        }
        {
          'id': 'Panasonic–TH55LF6U'
          'displayName': 'Panasonic – TH55LF6U'
        }
        {
          'id': 'Sharp-PNE521'
          'displayName': 'Sharp - PNE521'
        }
      ]

    getPanelInputs: () ->
      [
        {
          'id': 'son001'
          'displayName': '0x08 INPUT1 RGB (Analog)'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 'son002'
          'displayName': '0x09 INPUT1 YUV (Analog)'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 'son003'
          'displayName': '0x0C OPTION1 VIDEO'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 'son004'
          'displayName': '0x0D OPTION1 S-VIDEO'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 'son005'
          'displayName': '0x0E OPTION1 RGB'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 6
          'displayName': '0x0F OPTION1 COMPONENT 0x10 OPTION2 VIDEO*2'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 7
          'displayName': '0x11 OPTION2 S-VIDEO*2'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 8
          'displayName': '0x12 OPTION2 RGB*2'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 9
          'displayName': '0x13 OPTION2 COMPONENT*2'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 10
          'displayName': '0x44 INPUT2 RGB (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 11
          'displayName': '0x45 INPUT2 DTV (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 12
          'displayName': '0x54 INPUT3 RGB (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 13
          'displayName': '0x55 INPUT3 DTV (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }

        {
          'id': 14
          'displayName': '0x01 = VIDEO'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 15
          'displayName': '0x01 = S-VIDEO'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 16
          'displayName': '0x03 = COMPONENT'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 17
          'displayName': '0x05 = VGA'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 18
          'displayName': '0x05 = HDMI 2'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 19
          'displayName': '0x06 = Display Port 2'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 20
          'displayName': '0x06 = USB 2'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 21
          'displayName': '0x07 = Card DVI-D'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 22
          'displayName': '0x07 = Display Port or Display Port 1 0x08 = Card OPS'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 23
          'displayName': '0x08 = USB or USB 1'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 24
          'displayName': '0x09 = HDMI or HDMI 1'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 25
          'displayName': '0x09 = DVI-D'
          'parentId': 'Phillips–BDL5560EL'
        }

        {
          'id': 26
          'displayName': 'AV1 (VIDEO)'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 27
          'displayName': 'AV2 COMPONENT/RGB IN'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 28
          'displayName': 'HM1 HDMI 1'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 29
          'displayName': 'HM2 HDMI 2'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 30
          'displayName': 'DV1 DVI-D IN'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 31
          'displayName': 'PC1 PC IN'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 32
          'displayName': 'DL1 DIGITAL LINK'
          'parentId': 'Panasonic–TH55LF6U'
        }

        {
          'id': 33
          'displayName': 'PC-DVI-D'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 34
          'displayName': 'PC D-SUB'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 35
          'displayName': 'AV COMPONENT'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 36
          'displayName': 'AV VIDEO'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 37
          'displayName': 'PC RGB'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 38
          'displayName': 'AV DVI-D'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 39
          'displayName': 'AV S-VIDEO'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 40
          'displayName': 'AV HDMI'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 41
          'displayName': 'PC HDMI'
          'parentId': 'Sharp-PNE521'
        }

        {
          'id': 42
          'displayName': 'TBD'
          'parentId': 'NEC–LCD4215'
        }
      ]


  new DevicesService()
