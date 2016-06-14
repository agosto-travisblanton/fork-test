'use strict'

describe 'AdminCtrl', ->
  beforeEach module('skykitProvisioning')

  $controller = undefined
  controller = undefined
  ToastsService = undefined
  $mdDialog = undefined
  AdminService = undefined
  DistributorsService = undefined
  SessionsService = undefined
  getAllDistributorsPromise = undefined
  angularForm = undefined
  getUsersOfDistributorPromise = undefined
  currentDistributorName = 'current'

  beforeEach inject (_$controller_, _$mdDialog_, _ToastsService_, _DistributorsService_, _SessionsService_, _AdminService_) ->
    $controller = _$controller_
    SessionsService = _SessionsService_
    ToastsService = _ToastsService_
    AdminService = _AdminService_
    DistributorsService = _DistributorsService_
    $mdDialog = _$mdDialog_

  describe '.initialize', ->
    beforeEach ->
      controller = $controller 'AdminCtrl', {
        SessionsService: SessionsService,
        ToastsService: ToastsService,
        DistributorsService: DistributorsService
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
      spyOn(SessionsService, 'getCurrentDistributorName').and.returnValue currentDistributorName
      spyOn(SessionsService, 'getCurrentDistributorKey').and.returnValue []

      spyOn(AdminService, 'getUsersOfDistributor').and.returnValue getUsersOfDistributorPromise
      spyOn(AdminService, 'addUserToDistributor').and.returnValue addUserToDistributorPromise
      spyOn(AdminService, 'makeDistributor').and.returnValue makeDistributorPromise
      spyOn(AdminService, 'getAllDistributors').and.returnValue getAllDistributorsPromise
      spyOn($mdDialog, 'show').and.returnValue mdDialogPromise

      spyOn($mdDialog, 'confirm').and.callFake -> return 'ok'

      angularForm = {
        $setPristine: () ->

        $setUntouched: () ->
      }

    it '.getsAllDistributors', ->
      controller.getAllDistributors()
      expect(controller.loadingAllDistributors).toBe true
      distributors = ["one", "two"]
      getAllDistributorsPromise.resolve(distributors)
      expect(controller.loadingAllDistributors).toBe false
      expect(controller.allDistributors).toEqual distributors

    it '.addUserToDistributor', ->
      jquery_event = {}
      userEmail = {email: "test@gmail.com"}
      distributorAdmin = false
      whichDistributor = "someDistributor"
      withOrWithout = if distributorAdmin then "with" else "without"
      controller.addUserToDistributor jquery_event, userEmail, distributorAdmin, whichDistributor, angularForm
      confirm = $mdDialog.confirm(
        {
          title: 'Are you sure?'
          textContent: "#{userEmail} will be added to #{whichDistributor}
      #{withOrWithout} administrator priviledges"
          targetEvent: jquery_event
          ok: 'Of course!'
          cancel: 'Oops, nevermind.'
        }
      )
      expect($mdDialog.show).toHaveBeenCalledWith confirm
      expect(AdminService.addUserToDistributor).toHaveBeenCalled


    it '.makeDistributor', ->
      jquery_event = {}
      adminEmail = {email: "test@gmail.com"}
      distributorName = "someDistributor"
      controller.makeDistributor jquery_event, distributorName, adminEmail, angularForm
      confirm = $mdDialog.confirm(
        {
          title: 'Are you sure?'
          textContent: "If you proceed, #{distributorName} will be created."
          targetEvent: jquery_event
          ariaLabel: 'Lucky day'
          ok: 'Yeah!'
          cancel: 'Forget it.'
        }
      )
      expect($mdDialog.show).toHaveBeenCalledWith confirm
      expect(AdminService.makeDistributor).toHaveBeenCalled

    it '.getUsersOfDistributor', ->
      controller.getUsersOfDistributor()
      expect(controller.loadingUsersOfDistributor).toBe true

    it '.switchDistributor', ->
      distributor = {name: "test"}
      controller.switchDistributor(distributor)
      expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
        "Distributor #{distributor.name} selected!")
  
    it '.initialize', ->
      controller.initialize()
      expect(controller.currentDistributorName).toEqual currentDistributorName
      expect(controller.isAdmin).toEqual true
      expect(controller.distributorsAsAdmin).toEqual []
