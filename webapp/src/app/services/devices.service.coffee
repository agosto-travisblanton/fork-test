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
      device.panelModel = device.panelModel.id if device.panelModel != null
      device.panelInput = device.panelInput.id if device.panelInput != null
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
          'id': 'son1'
          'displayName': '0x08 INPUT1 RGB (Analog)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son2'
          'displayName': '0x09 INPUT1 YUV (Analog)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son3'
          'displayName': '0x0C OPTION1 VIDEO'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son4'
          'displayName': '0x0D OPTION1 S-VIDEO'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son5'
          'displayName': '0x0E OPTION1 RGB'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son6'
          'displayName': '0x0F OPTION1 COMPONENT 0x10 OPTION2 VIDEO*2'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son7'
          'displayName': '0x11 OPTION2 S-VIDEO*2'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son8'
          'displayName': '0x12 OPTION2 RGB*2'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son9'
          'displayName': '0x13 OPTION2 COMPONENT*2'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son10'
          'displayName': '0x44 INPUT2 RGB (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son11'
          'displayName': '0x45 INPUT2 DTV (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son12'
          'displayName': '0x54 INPUT3 RGB (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'son13'
          'displayName': '0x55 INPUT3 DTV (Digital)'
          'parentId': 'Sony–FXD40LX2F'
        }
        {
          'id': 'phi1'
          'displayName': '0x01 = VIDEO'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi2'
          'displayName': '0x01 = S-VIDEO'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi3'
          'displayName': '0x03 = COMPONENT'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi4'
          'displayName': '0x05 = VGA'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi5'
          'displayName': '0x05 = HDMI 2'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi6'
          'displayName': '0x06 = Display Port 2'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi7'
          'displayName': '0x06 = USB 2'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi8'
          'displayName': '0x07 = Card DVI-D'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi9'
          'displayName': '0x07 = Display Port or Display Port 1 0x08 = Card OPS'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi10'
          'displayName': '0x08 = USB or USB 1'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi11'
          'displayName': '0x09 = HDMI or HDMI 1'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'phi12'
          'displayName': '0x09 = DVI-D'
          'parentId': 'Phillips–BDL5560EL'
        }
        {
          'id': 'pan1'
          'displayName': 'AV1 (VIDEO)'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'pan2'
          'displayName': 'AV2 COMPONENT/RGB IN'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'pan3'
          'displayName': 'HM1 HDMI 1'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'pan4'
          'displayName': 'HM2 HDMI 2'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'pan5'
          'displayName': 'DV1 DVI-D IN'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'pan6'
          'displayName': 'PC1 PC IN'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'pan7'
          'displayName': 'DL1 DIGITAL LINK'
          'parentId': 'Panasonic–TH55LF6U'
        }
        {
          'id': 'sha1'
          'displayName': 'PC-DVI-D'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha2'
          'displayName': 'PC D-SUB'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha3'
          'displayName': 'AV COMPONENT'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha4'
          'displayName': 'AV VIDEO'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha5'
          'displayName': 'PC RGB'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha6'
          'displayName': 'AV DVI-D'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha7'
          'displayName': 'AV S-VIDEO'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha8'
          'displayName': 'AV HDMI'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'sha9'
          'displayName': 'PC HDMI'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'nec1'
          'displayName': 'TBD'
          'parentId': 'NEC–LCD4215'
        }
      ]


  new DevicesService()
