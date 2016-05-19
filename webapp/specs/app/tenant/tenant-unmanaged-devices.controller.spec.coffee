'use strict'

describe 'TenantUnmanagedDevicesCtrl', ->
  scope = undefined
  $controller = undefined
  $state = undefined
  $stateParams = undefined
  TenantsService = undefined
  DevicesService = undefined
  ProgressBarService = undefined
  serviceInjection = undefined
  tenantsServicePromise = undefined
  controller = undefined
  partial = undefined
  promise = undefined
  devicesServicePromise = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _TenantsService_, _DevicesService_, _$state_, _ProgressBarService_, _$rootScope_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    $rootScope = _$rootScope_
    TenantsService = _TenantsService_
    DevicesService = _DevicesService_
    ProgressBarService = _ProgressBarService_
    scope = $rootScope.$new()
    serviceInjection = {
      $scope: scope
      $stateParams: $stateParams
      TenantsService: TenantsService
      DevicesService: DevicesService
      ProgressBarService: ProgressBarService
    }

  describe 'initialization', ->
    beforeEach ->
      tenantsServicePromise = new skykitProvisioning.q.Mock
      devicesServicePromise = new skykitProvisioning.q.Mock
      spyOn(ProgressBarService, 'start')
      spyOn(ProgressBarService, 'complete')
      spyOn(TenantsService, 'getTenantByKey').and.returnValue tenantsServicePromise
      spyOn(DevicesService, 'getUnmanagedDevicesByTenant').and.returnValue devicesServicePromise

    it 'currentTenant should be set', ->
      controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
      expect(controller.currentTenant).toBeDefined()
      expect(controller.currentTenant.key).toBeUndefined()
      expect(controller.currentTenant.name).toBeUndefined()
      expect(controller.currentTenant.tenant_code).toBeUndefined()
      expect(controller.currentTenant.admin_email).toBeUndefined()
      expect(controller.currentTenant.content_server_url).toBeUndefined()
      expect(controller.currentTenant.domain_key).toBeUndefined()
      expect(controller.currentTenant.notification_emails).toBeUndefined()
      expect(controller.currentTenant.proof_of_play_logging).toBeFalsy()
      expect(controller.currentTenant.active).toBeTruthy()

    it 'tenantDevices property should be defined', ->
      controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
      expect(controller.tenantDevices).toBeDefined()

    describe 'editing an existing tenant', ->
      beforeEach ->
        progressBarService = {
          start: ->
          complete: ->
        }
        $stateParams = {tenantKey: 'fahdsfyudsyfauisdyfoiusydfu'}
        serviceInjection = {
          $scope: scope
          $stateParams: $stateParams
          ProgressBarService: progressBarService
        }
        promise = new skykitProvisioning.q.Mock
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection


      it 'editMode should be set to true', ->
        expect(controller.editMode).toBeTruthy()

      it 'retrieve tenant by key from TenantsService', ->
        tenant = {key: 'fahdsfyudsyfauisdyfoiusydfu', name: 'Foobar'}
        tenantsServicePromise.resolve(tenant)
        expect(TenantsService.getTenantByKey).toHaveBeenCalledWith($stateParams.tenantKey)
        expect(controller.currentTenant).toBe(tenant)

      it 'retrieve tenant\'s devices by tenant key from DevicesService', ->
        data = [1, 2, 3]
        devices = {"devices": data}
        devicesServicePromise.resolve(devices)
        expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith($stateParams.tenantKey, null, null)
        expect(controller.tenantDevices).toBe(data)

    describe 'creating a new tenant', ->
      it 'editMode should be set to false', ->
        $stateParams = {}
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(controller.editMode).toBeFalsy()

      it 'do not call TenantsService.getTenantByKey', ->
        $stateParams = {}
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(TenantsService.getTenantByKey).not.toHaveBeenCalled()

      it 'do not call Devices.getUnmanagedDevicesByTenant', ->
        $stateParams = {}
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
        expect(DevicesService.getUnmanagedDevicesByTenant).not.toHaveBeenCalled()

    describe 'editItem', ->
      controller = undefined
      tenantKey = 'bhjad897d987fa32fg708fg72'
      item = {key: 'ahjad897d987fadafg708fg71'}

      beforeEach ->
        spyOn $state, 'go'
        $stateParams = {tenantKey: tenantKey}
        serviceInjection = {
          $scope: scope
          $stateParams: $stateParams
        }
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection

      it "route to the 'editDevice' named route, passing the supplied device key", ->
        controller.editItem(item)
        expect($state.go).toHaveBeenCalledWith('editDevice', {
          deviceKey: item.key,
          tenantKey: tenantKey,
          fromDevices: false
        })

    describe 'search and pagination ', ->
      beforeEach ->
        spyOn $state, 'go'
        tenantKey = 'bhjad897d987fa32fg708fg72'
        $stateParams = {tenantKey: tenantKey}
        serviceInjection = {
          $scope: scope
          $stateParams: $stateParams
        }

        partial = "some text"
        promise = new skykitProvisioning.q.Mock
        spyOn(DevicesService, 'searchDevicesByPartialMacByTenant').and.returnValue promise
        spyOn(DevicesService, 'searchDevicesByPartialSerialByTenant').and.returnValue promise
        controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection


      convertArrayToDictionary = (theArray, mac) ->
        Devices = {}
        for item in theArray
          if mac
            Devices[item.mac] = item
          else
            Devices[item.serial] = item

        return Devices


      it "returns every serial name when called as an managed serial", ->
        controller.selectedButton = "Serial Number"
        controller.searchDevices(partial)
        serial_matches = {
          "serial_number_matches": [
            {"serial": "1234"},
            {"serial": "45566"}
          ]
        }
        promise.resolve serial_matches
        expect(controller.serialDevices).toEqual convertArrayToDictionary(serial_matches["serial_number_matches"], false)

      it "returns every serial name when called as an managed mac", ->
        controller.selectedButton = "MAC"
        controller.searchDevices(partial)
        mac_matches = {
          "mac_matches": [
            {"mac": "1234"},
            {"mac": "45566"}
          ]
        }
        promise.resolve mac_matches
        expect(controller.macDevices).toEqual convertArrayToDictionary(mac_matches["mac_matches"], true)

      it 'resets variables whenever function is called', ->
        controller.changeRadio()
        expect(controller.searchText).toEqual ''
        expect(controller.disabled).toEqual true
        expect(controller.serialDevices).toEqual {}
        expect(controller.macDevices).toEqual {}

      it 'paginates forward', ->
        controller.paginateCall(true)
        expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith controller.tenantKey, null, controller.devicesNext

      it 'paginates backward', ->
        controller.paginateCall(false)
        expect(DevicesService.getUnmanagedDevicesByTenant).toHaveBeenCalledWith controller.tenantKey, controller.devicesPrev, null


      describe '.prepareForEditItem', ->
        resourceSearch = "test"

        beforeEach ->
          controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
          controller.macDevices = {"test": {"key": "1234", "tenantKey": "5678"}}
          controller.serialDevices = {"test": {"key": "1234", "tenantKey": "5678"}}


        it "prepares for editItem as", ->
          controller.selectedButton == "MAC"
          controller.prepareForEditView(resourceSearch)
          expect($state.go).toHaveBeenCalledWith('editDevice', {
            deviceKey: controller.macDevices[resourceSearch].key,
            tenantKey: controller.tenantKey,
            fromDevices: false
          })

        it "prepares for editItem as serial", ->
          controller.selectedButton == "Serial Number"
          controller.prepareForEditView(resourceSearch)
          expect($state.go).toHaveBeenCalledWith('editDevice', {
            deviceKey: controller.serialDevices[resourceSearch].key,
            tenantKey: controller.tenantKey,
            fromDevices: false
          })

      describe '.isResourceValid', ->
        resource = 'my-resource'

        beforeEach ->
          tenantKey = 'bhjad897d987fa32fg708fg72'
          $stateParams = {tenantKey: tenantKey}
          serviceInjection = {
            $scope: scope
            $stateParams: $stateParams
          }
          controller = $controller 'TenantUnmanagedDevicesCtrl', serviceInjection
          promise = new skykitProvisioning.q.Mock
          spyOn(DevicesService, 'matchDevicesByFullMacByTenant').and.returnValue promise
          spyOn(DevicesService, 'matchDevicesByFullSerialByTenant').and.returnValue promise

        it "matchDevicesByFullMac called when managed and button is mac", ->
          controller.selectedButton = "MAC"
          controller.isResourceValid(resource)
          promise.resolve false
          expect(DevicesService.matchDevicesByFullMacByTenant).toHaveBeenCalledWith controller.tenantKey, resource, true

        it "matchDevicesByFullSerial called button is not mac", ->
          controller.selectedButton = "Serial Number"
          controller.isResourceValid(resource)
          promise.resolve false
          expect(DevicesService.matchDevicesByFullSerialByTenant).toHaveBeenCalledWith controller.tenantKey, resource, true
  
  
