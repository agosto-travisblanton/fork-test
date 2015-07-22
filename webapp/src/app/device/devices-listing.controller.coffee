'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DevicesListingCtrl', ($stateParams, DevicesService) ->

  @devices = []

  initialize: ->


  @
