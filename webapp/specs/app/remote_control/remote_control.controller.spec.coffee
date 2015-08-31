'use strict'

describe 'RemoteControlCtrl', ->
  scope = undefined
  $controller = undefined
  controller = undefined
  $state = undefined
  $stateParams = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    $stateParams = {}
    scope = {}

  describe 'initialization', ->
    beforeEach ->
      controller = $controller('RemoteControlCtrl', {$scope: scope, $stateParams: $stateParams})

    describe 'devices instance variable', ->
      it 'is an array', ->
        expect(controller.devices instanceof Array).toBeTruthy()

      it 'is empty', ->
        expect(controller.devices.length).toBe 0

    describe 'currentDevice instance variable', ->
      it 'is an Object', ->
        expect(controller.currentDevice instanceof Object).toBeTruthy()

      it 'id property is undefined', ->
        expect(controller.currentDevice.id).toBeUndefined()

      it 'name property is undefined', ->
        expect(controller.currentDevice.name).toBeUndefined()

    describe '.initialize', ->
      beforeEach ->
        controller.initialize()

      it 'sets the devices instance variable', ->
        expect(controller.devices.length).toBe 4


