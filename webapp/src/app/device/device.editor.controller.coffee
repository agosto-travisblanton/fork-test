'use strict'

angular.module "skykitDisplayDeviceManagement"
.controller "DeviceEditorCtrl", ($scope, $log, sweet, DevicesService) ->

  @onClickSaveButton = () ->
    sweet.show 'Sweet Jebus', 'You\'ve done it!', 'success'


  @
