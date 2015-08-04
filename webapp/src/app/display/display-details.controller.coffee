'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DisplayDetailsCtrl', ($stateParams, DisplaysService) ->
  @currentDisplay = {
    key: undefined
    gcmRegistrationId: undefined
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
    tenantCode: undefined #"foobar_inc"
    created: undefined #"2015-07-07 19:22:57"
    updated: undefined #"2015-07-07 19:22:57"
  }
  @editMode = !!$stateParams.displayKey

  if @editMode
    displayPromise = DisplaysService.getDisplayByKey($stateParams.displayKey)
    displayPromise.then (data) =>
      @currentDisplay = data

  @onClickSaveButton = () ->
#    promise = DisplaysService.save @currentDisplay
#    promise.then (data) ->
#      $state.go 'displays'


  @
