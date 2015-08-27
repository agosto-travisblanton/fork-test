'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DeviceDetailsCtrl', ($stateParams, $state, DevicesService, TenantsService) ->
  @tenantKey = $stateParams.tenantKey

  @currentDevice = {
    key: undefined
    gcmRegistrationId: undefined
    annotatedLocation: undefined
    annotatedUser: undefined
    apiKey: undefined
    deviceId: undefined #"41b0f043-4296-4c56-b21a-c8bd660ea9ca"
    bootMode: undefined
    chromeDeviceDomain: undefined
    contentServerUrl: undefined
    etag: undefined
    ethernetMacAddress: undefined #"3863bb98f982"
    macAddress: undefined #"38b1db95ac21"
    firmwareVersion: undefined #""
    kind: undefined #"admin#directory#chromeosdevice"
    lastEnrollmentTime: undefined #"2015-05-06T20:01:31.459Z"
    lastSync: undefined #"2015-07-07T17:38:14.274Z"
    model: undefined #"HP Chromebox CB1-(000-099) / HP Chromebox G1"
    orgUnitPath: undefined #"/Beta/Fairchild Semi"
    osVersion: undefined #"42.0.2311.153"
    platformVersion: undefined #"6812.88.0 (Official Build) stable-channel zako"
    serialNumber: undefined #"5CD45183T6"
    status: undefined #"ACTIVE"
    tenantKey: undefined
    created: undefined #"2015-07-07 19:22:57"
    updated: undefined #"2015-07-07 19:22:57"
  }
  @editMode = !!$stateParams.deviceKey

  tenantsPromise = TenantsService.fetchAllTenants()
  tenantsPromise.then (data) =>
    @tenants = data


  if @editMode
    devicePromise = DevicesService.getDeviceByKey($stateParams.deviceKey)
    devicePromise.then (data) =>
      @currentDevice = data

  @onClickSaveButton = () ->
    promise = DevicesService.save @currentDevice
    promise.then (data) ->
      $state.go 'devices'

  @
