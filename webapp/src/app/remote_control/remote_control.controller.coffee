'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "RemoteControlCtrl", (DevicesService) ->
  @devices = []
  @currentDevice = {
    id: undefined,
    name: undefined
  }

  @initialize = ->
    @devices =
      [
        {id: 1, name: "Device 1"},
        {id: 2, name: "Device 2"},
        {id: 3, name: "Device 3"},
        {id: 4, name: "Device 4"}
      ]

  @

