'use strict'

angular.module "skykitDisplayDeviceManagement"
.controller "DeviceEditorCtrl", ($scope, $log, sweet) ->

  @onClickSaveButton = () ->
    sweet.show 'Sweet Jebus', 'You\'ve done it!', 'success'


  @
