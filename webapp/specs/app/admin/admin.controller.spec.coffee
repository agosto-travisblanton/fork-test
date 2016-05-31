'use strict'

describe 'AdminCtrl', ->
  beforeEach module('skykitProvisioning')

  $controller = undefined
  controller = undefined
  ToastsService = undefined
  $mdDialog = undefined
  AdminService = undefined
  SessionsService = undefined
  getAllDistributorsPromise = undefined

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

      getAllDistributorsPromise = new skykitProvisioning.q.Mock
      mdDialogPromise = new skykitProvisioning.q.Mock
      addUserToDistributorPromise = new skykitProvisioning.q.Mock
      makeDistributorPromise = new skykitProvisioning.q.Mock
      getUsersOfDistributorPromise = new skykitProvisioning.q.Mock

      spyOn(ToastsService, 'showSuccessToast')
      spyOn(ToastsService, 'showErrorToast')
      spyOn(DistributorsService, 'switchDistributor')

      spyOn(SessionsService, 'getIsAdmin').and.returnValue true
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue []
      spyOn(SessionsService, 'getCurrentDistributorName').and.returnValue []

      spyOn(AdminService, 'getUsersOfDistributor').and.returnValue getUsersOfDistributorPromise
      spyOn(AdminService, 'addUserToDistributor').and.returnValue addUserToDistributorPromise
      spyOn(AdminService, 'makeDistributor').and.returnValue makeDistributorPromise
      spyOn(AdminService, 'getAllDistributors').and.returnValue getAllDistributorsPromise
      spyOn($mdDialog, 'show').and.returnValue mdDialogPromise

      spyOn($mdDialog, 'confirm').and.callFake -> return 'ok'

