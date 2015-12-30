'use strict'

describe 'NavbarCtrl', ->
  $controller = undefined
  controller = undefined
  VersionsService = undefined

  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _VersionsService_) ->
    $controller = _$controller_
    VersionsService = _VersionsService_

  describe 'initialization', ->
    beforeEach ->
      controller = $controller 'NavbarCtrl', {
        VersionsService: VersionsService
      }

    it 'creates a controller instance', ->
      expect(controller).toBeDefined()

