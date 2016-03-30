'use strict'


describe 'DevicesListingCtrl', ->
  $controller = undefined
  controller = undefined
  $stateParams = undefined
  $state = undefined
  DevicesService = undefined
  promise = undefined
  unmanagedPromise = undefined
  ProgressBarService = undefined
  serialPromise = undefined
  sweet = undefined

  to_respond_with_devices = {
    devices: [
      {key: 'dhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'dhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]
  }
  to_respond_with_unmanagedDevices = {
    unmanagedDevices: [
      {key: 'uhjad897d987fadafg708fg7d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'uhjad897d987fadafg708y67d', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
      {key: 'uhjad897d987fadafg708hb55', created: '2015-05-10 22:15:10', updated: '2015-05-10 22:15:10'}
    ]
  }

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _DevicesService_, _$stateParams_, _$state_, _ProgressBarService_, _sweet_) ->
    $controller = _$controller_
    $stateParams = _$stateParams_
    DevicesService = _DevicesService_
    $state = _$state_
    ProgressBarService = _ProgressBarService_
    sweet = _sweet_

  describe 'initialization', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      unmanagedPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue promise
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue unmanagedPromise
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')
      controller = $controller 'DevicesListingCtrl', {}
      controller.distributorKey = 'some-key'

    it 'devices should be an array', ->
      expect(angular.isArray(controller.devices)).toBeTruthy()

    it 'unmanagedDevices should be an array', ->
      expect(angular.isArray(controller.unmanagedDevices)).toBeTruthy()

    it 'calls DevicesService.getDevicesByDistributor to retrieve all distributor devices', ->
      controller.initialize()
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.devicesPrev, controller.devicesNext

    it 'starts the progress bar', ->
      controller.initialize()
      promise.resolve to_respond_with_devices
      unmanagedPromise.resolve to_respond_with_unmanagedDevices
      expect(controller.devices).toBe to_respond_with_devices.devices
      expect(controller.unmanagedDevices).toBe to_respond_with_unmanagedDevices.devices
      expect(ProgressBarService.start).toHaveBeenCalled()

    it 'calls DevicesService.getUnmanagedDevicesByDistributor to retrieve all distributor unmanaged devices', ->
      controller.initialize()
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.unmanagedDevicesPrev, controller.unmanagedDevicesNext

  describe '.getFetchSuccess', ->
    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      controller = $controller 'DevicesListingCtrl', {}

    it 'stops the progress bar', ->
      controller.getFetchSuccess()
      expect(ProgressBarService.complete).toHaveBeenCalled()

  describe '.getFetchFailure', ->
    response = {status: 400, statusText: 'Bad request'}
    beforeEach ->
      spyOn(ProgressBarService, 'complete')
      spyOn(sweet, 'show')
      controller = $controller 'DevicesListingCtrl', {}

    it 'stops the progress bar', ->
      controller.getFetchFailure response
      expect(ProgressBarService.complete).toHaveBeenCalled()

    it 'calls seet alert with error', ->
      controller.getFetchFailure response
      expect(sweet.show).toHaveBeenCalledWith('Oops...', 'Unable to fetch devices. Error: 400 Bad request.', 'error')

  describe '.editItem', ->
    item = {key: 'ahjad897d987fadafg708fg71', tenantKey: 'ahjad897d987fadafg708fg71', fromDevices: true}

    beforeEach ->
      spyOn $state, 'go'
      controller = $controller 'DevicesListingCtrl', {}

    it "route to the 'editDevice' named route, passing the supplied device key", ->
      controller.editItem(item)
      expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: item.key,
        tenantKey: item.tenantKey,
        fromDevices: true
      })

  describe '.paginateCall', ->
    beforeEach ->
      spyOn $state, 'go'
      promise = new skykitProvisioning.q.Mock
      unmanagedPromise = new skykitProvisioning.q.Mock
      spyOn(DevicesService, 'getDevicesByDistributor').and.returnValue promise
      spyOn(DevicesService, 'getUnmanagedDevicesByDistributor').and.returnValue unmanagedPromise
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')
      controller = $controller 'DevicesListingCtrl', {}
      controller.devicesPrev = '1'
      controller.devicesNext = '2'
      controller.unmanagedDevicesPrev = '3'
      controller.unmanagedDevicesNext = '4'
      controller.distributorKey = 'some-key'

    it "paginated forward with unmanaged", ->
      controller.paginateCall(true, false)
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, null, controller.unmanagedDevicesNext

    it 'paginates forward with managed', ->
      controller.paginateCall(true, true)
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, null, controller.devicesNext


    it "paginated backward with unmanaged", ->
      controller.paginateCall(false, false)
      expect(DevicesService.getUnmanagedDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.unmanagedDevicesPrev, null

    it 'paginates backward with managed', ->
      controller.paginateCall(false, true)
      expect(DevicesService.getDevicesByDistributor).toHaveBeenCalledWith controller.distributorKey, controller.devicesPrev, null

  describe '.search bar related functions', ->
    beforeEach ->
      controller = $controller 'DevicesListingCtrl', {}

    it 'resets variables whenever function is called with unmanaged', ->
      unmanaged = true
      controller.changeRadio(unmanaged)

      expect(controller.unmanagedSearchText).toEqual ''
      expect(controller.unmanagedDisabled).toEqual true
      expect(controller.unmanagedSerialDevices).toEqual {}
      expect(controller.unmanagedMacDevices).toEqual {}

    it 'resets variables whenever function is called with managed', ->
      unmanaged = false
      controller.changeRadio(unmanaged)

      expect(controller.searchText).toEqual ''
      expect(controller.disabled).toEqual true
      expect(controller.serialDevices).toEqual {}
      expect(controller.macDevices).toEqual {}


    it 'converts array to dictionary with serial as key', ->
      theArray = [{"serial": "test", "a": "b"}]
      isMac = false
      result = controller.convertArrayToDictionary(theArray, isMac)
      expect(result).toEqual {"test": {"a": "b", "serial": "test"}}


    it 'converts array to dictionary with mac key', ->
      theArray = [{"mac": "test", "a": "b"}]
      isMac = true
      result = controller.convertArrayToDictionary(theArray, isMac)
      expect(result).toEqual {"test": {"a": "b", "mac": "test"}}


  describe '.prepareForEditItem', ->
    resourceSearch = "test"

    beforeEach ->
      spyOn $state, 'go'
      controller = $controller 'DevicesListingCtrl', {}
      controller.unmanagedMacDevices = {"test": {"key": "1234", "tenantKey": "5678"}}
      controller.unmanagedSerialDevices = {"test": {"key": "1234", "tenantKey": "5678"}}
      controller.macDevices = {"test": {"key": "1234", "tenantKey": "5678"}}
      controller.serialDevices = {"test": {"key": "1234", "tenantKey": "5678"}}

    it "prepares for editItem as unmanaged mac", ->
      controller.unmanagedSelectedButton == "MAC"
      unmanaged = true
      controller.prepareForEditView(unmanaged, resourceSearch)
      expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.unmanagedMacDevices[resourceSearch].key,
        tenantKey: controller.unmanagedMacDevices[resourceSearch].tenantKey,
        fromDevices: true
      })

    it "prepares for editItem as unmanaged serial;", ->
      controller.unmanagedSelectedButton == "Serial Number"
      unmanaged = true
      controller.prepareForEditView(unmanaged, resourceSearch)
      expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.unmanagedMacDevices[resourceSearch].key,
        tenantKey: controller.unmanagedMacDevices[resourceSearch].tenantKey,
        fromDevices: true
      })

    it "prepares for editItem as managed mac", ->
      controller.selectedButton == "MAC"
      unmanaged = false
      controller.prepareForEditView(unmanaged, resourceSearch)
      expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.macDevices[resourceSearch].key,
        tenantKey: controller.macDevices[resourceSearch].tenantKey,
        fromDevices: true
      })

    it "prepares for editItem as managed serial", ->
      controller.selectedButton == "Serial Number"
      unmanaged = false
      controller.prepareForEditView(unmanaged, resourceSearch)
      expect($state.go).toHaveBeenCalledWith('editDevice', {
        deviceKey: controller.serialDevices[resourceSearch].key,
        tenantKey: controller.serialDevices[resourceSearch].tenantKey,
        fromDevices: true
      })

  describe '.controlOpenButton', ->
    beforeEach ->
      controller = $controller 'DevicesListingCtrl', {}

    it "unmanagedDisabled is false if unmanaged and a match", ->
      isMatch = true
      unmanaged = true
      controller.controlOpenButton(unmanaged, isMatch)
      expect(controller.unmanagedDisabled).toBeFalsy()

    it "unmanagedDisabled is true if unmanaged and a not match", ->
      isMatch = false
      unmanaged = true
      controller.controlOpenButton(unmanaged, isMatch)
      expect(controller.unmanagedDisabled).toBeTruthy()


    it "disabled is false if managed and a match", ->
      isMatch = true
      unmanaged = false
      controller.controlOpenButton(unmanaged, isMatch)
      expect(controller.disabled).toBeFalsy()

    it "disabled is true if managed and a match", ->
      isMatch = false
      unmanaged = false
      controller.controlOpenButton(unmanaged, isMatch)
      expect(controller.disabled).toBeTruthy()


  describe '.isResourceValid', ->
    resource = 'my-resource'

    beforeEach ->
      controller = $controller 'DevicesListingCtrl', {}
      promise = new skykitProvisioning.q.Mock
      serialPromise = new skykitProvisioning.q.Mock

      spyOn(DevicesService, 'matchDevicesByFullMac').and.returnValue promise
      spyOn(DevicesService, 'matchDevicesByFullSerial').and.returnValue serialPromise

    it "matchDevicesByFullMac called when unmanaged and button is mac", ->
      unmanaged = true
      controller.unmanagedSelectedButton = "MAC"
      controller.isResourceValid(unmanaged, resource)
      promise.resolve false
      expect(DevicesService.matchDevicesByFullMac).toHaveBeenCalledWith controller.distributorKey, resource, unmanaged

    it "matchDevicesByFullSerial called when unmanaged and button is not mac", ->
      unmanaged = true
      controller.unmanagedSelectedButton = "Serial Number"
      controller.isResourceValid(unmanaged, resource)
      serialPromise.resolve false
      expect(DevicesService.matchDevicesByFullSerial).toHaveBeenCalledWith controller.distributorKey, resource, unmanaged

    it "matchDevicesByFullMac called when managed and button is mac", ->
      unmanaged = false
      controller.selectedButton = "MAC"
      controller.isResourceValid(unmanaged, resource)
      promise.resolve false
      expect(DevicesService.matchDevicesByFullMac).toHaveBeenCalledWith controller.distributorKey, resource, unmanaged

    it "matchDevicesByFullSerial called when managed and button is not mac", ->
      unmanaged = false
      controller.selectedButton = "Serial Number"
      controller.isResourceValid(unmanaged, resource)
      serialPromise.resolve false
      expect(DevicesService.matchDevicesByFullSerial).toHaveBeenCalledWith controller.distributorKey, resource, unmanaged

  describe '.searchDevices', ->
    partial = "it doesn't matter dwight!"
    beforeEach ->
      controller = $controller 'DevicesListingCtrl', {}
      promise = new skykitProvisioning.q.Mock
      serialPromise = new skykitProvisioning.q.Mock

      spyOn(DevicesService, 'searchDevicesByPartialMac').and.returnValue promise
      spyOn(DevicesService, 'searchDevicesByPartialSerial').and.returnValue serialPromise

    convertArrayToDictionary = (theArray, mac) ->
      Devices = {}
      for item in theArray
        if mac
          Devices[item.mac] = item
        else
          Devices[item.serial] = item

      return Devices

    it "returns every serial name when called as an unmanaged serial", ->
      unmanaged = true
      controller.unmanagedSelectedButton = "Serial Number"
      controller.searchDevices(unmanaged, partial)
      serial_matches = {
        "serial_number_matches": [
          {"serial": "1234"},
          {"serial": "45566"}
        ]
      }
      serialPromise.resolve serial_matches
      expect(controller.unmanagedSerialDevices).toEqual convertArrayToDictionary(serial_matches["serial_number_matches"], false)

    it "returns every serial name when called as an unmanaged mac", ->
      unmanaged = true
      controller.unmanagedSelectedButton = "MAC"
      controller.searchDevices(unmanaged, partial)
      mac_matches = {
        "mac_matches": [
          {"mac": "1234"},
          {"mac": "45566"}
        ]
      }
      promise.resolve mac_matches
      expect(controller.unmanagedMacDevices).toEqual convertArrayToDictionary(mac_matches["mac_matches"], true)

    it "returns every serial name when called as an managed serial", ->
      unmanaged = false
      controller.selectedButton = "Serial Number"
      controller.searchDevices(unmanaged, partial)
      serial_matches = {
        "serial_number_matches": [
          {"serial": "1234"},
          {"serial": "45566"}
        ]
      }
      serialPromise.resolve serial_matches
      expect(controller.serialDevices).toEqual convertArrayToDictionary(serial_matches["serial_number_matches"], false)

    it "returns every mac name when called as an managed mac", ->
      unmanaged = false
      controller.selectedButton = "MAC"
      controller.searchDevices(unmanaged, partial)
      mac_matches = {
        "mac_matches": [
          {"mac": "1234"},
          {"mac": "45566"}
        ]
      }
      promise.resolve mac_matches
      expect(controller.macDevices).toEqual convertArrayToDictionary(mac_matches["mac_matches"], true)

#    it "matchDevicesByFullMac called when managed and button is mac", ->
#      unmanaged = false
#      controller.selectedButton = "MAC"
#      controller.isResourceValid(unmanaged, resource)
#      promise.resolve false
#      expect(DevicesService.matchDevicesByFullMac).toHaveBeenCalledWith controller.distributorKey, resource, unmanaged
#
#    it "matchDevicesByFullSerial called when managed and button is not mac", ->
#      unmanaged = false
#      controller.selectedButton = "Serial Number"
#      controller.isResourceValid(unmanaged, resource)
#      serialPromise.resolve false
#      expect(DevicesService.matchDevicesByFullSerial).toHaveBeenCalledWith controller.distributorKey, resource, unmanaged
#      
#
