'use strict'

angular.module "skykitDisplayDeviceManagement"
.controller "DeviceEditorCtrl", ($scope, $log, sweet) ->

  @onClickSaveButton = () ->
    $log.info 'Hello?'
    sweet.show 'Sweet Jebus', 'You\'ve done it!', 'success'


  @
