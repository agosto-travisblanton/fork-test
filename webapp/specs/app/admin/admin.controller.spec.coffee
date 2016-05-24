'use strict'

describe 'AdminCtrl', ->
  beforeEach module('skykitProvisioning')

  $controller = undefined
  controller = undefined
  ToastsService = undefined
  $mdDialog = undefined
  AdminService = undefined
  SessionsService = undefined

  beforeEach inject (_$controller_, _$mdDialog_, _ToastsService_, _SessionsService_, _AdminService_) ->
    $controller = _$controller_
    SessionsService = _SessionsService_
    ToastsService = _ToastsService_
    AdminService = _AdminService_
    $mdDialog = _$mdDialog_

  describe '.initialize', ->
    beforeEach ->
      controller = $controller 'AdminCtrl', {
        SessionsService: SessionsService,
        ToastsService: ToastsService,
        $mdDialog: $mdDialog,
        AdminService: AdminService
      }
