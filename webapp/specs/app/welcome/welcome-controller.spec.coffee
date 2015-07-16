'use strict'

describe 'WelcomeCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  promise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _$state_) ->
    $controller = _$controller_
    $state = _$state_
    controller = $controller 'WelcomeCtrl', {$state: $state}




