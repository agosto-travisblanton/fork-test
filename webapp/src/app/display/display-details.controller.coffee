'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DisplayDetailsCtrl', ($stateParams, DisplaysService) ->
  @currentDisplay = {
    key: undefined
    gcm_registration_id: undefined
    annotated_user: undefined
    api_key: undefined
    device_id: undefined #"41b0f043-4296-4c56-b21a-c8bd660ea9ca"
    boot_mode: undefined
    chrome_device_domain: undefined
    content_server_url: undefined
    etag: undefined
    ethernet_mac_address: undefined #"3863bb98f982"
    mac_address: undefined #"38b1db95ac21"
    firmware_version: undefined #""
    kind: undefined #"admin#directory#chromeosdevice"
    last_enrollment_time: undefined #"2015-05-06T20:01:31.459Z"
    last_sync: undefined #"2015-07-07T17:38:14.274Z"
    model: undefined #"HP Chromebox CB1-(000-099) / HP Chromebox G1"
    org_unit_path: undefined #"/Beta/Fairchild Semi"
    os_version: undefined #"42.0.2311.153"
    platform_version: undefined #"6812.88.0 (Official Build) stable-channel zako"
    serial_number: undefined #"5CD45183T6"
    status: undefined #"ACTIVE"
    tenant: undefined
    created: undefined #"2015-07-07 19:22:57"
    updated: undefined #"2015-07-07 19:22:57"
  }
  @editMode = !!$stateParams.displayKey

  if @editMode
    displayPromise = DisplaysService.getByKey($stateParams.displayKey)
    displayPromise.then (data) =>
      @currentDisplay = data

  @onClickSaveButton = () ->
#    promise = DisplaysService.save @currentDisplay
#    promise.then (data) ->
#      $state.go 'displays'


  @
