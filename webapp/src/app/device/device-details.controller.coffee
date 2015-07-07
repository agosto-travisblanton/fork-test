'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DeviceDetailsCtrl', ($stateParams, DevicesService) ->
  @currentDevice = {
    key: undefined
  }
  @editMode = !!$stateParams.deviceKey

  if @editMode
    devicePromise = DevicesService.getDeviceByKey($stateParams.deviceKey)
    devicePromise.then (data) =>
      @currentDevice = data

  @onClickSaveButton = () ->
#    promise = DevicesService.save @currentDevice
#    promise.then (data) ->
#      $state.go 'devices'


  @
