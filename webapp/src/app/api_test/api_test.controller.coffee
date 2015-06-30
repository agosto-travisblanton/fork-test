'use strict'

angular.module "skykitDisplayDeviceManagement"
.controller "ApiTestCtrl", ($scope, $log, sweet, DevicesService) ->
  @macAddress = undefined

  @onClickFindByMacAddressButton = ->
    device = DevicesService.getDeviceByMacAddress(@macAddress)
    sweet.show 'Success!', JSON.stringify(device), 'success'

  @
