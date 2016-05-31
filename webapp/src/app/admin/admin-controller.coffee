'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService,
  SessionsService,
  ToastsService,
  $mdDialog,
  DistributorsService) ->
  vm = @

  vm.getAllDistributors = () ->
    vm.loadingAllDistributors = true
    getAllDistributorsPromise = AdminService.getAllDistributors()
    getAllDistributorsPromise.then (data) ->
      vm.loadingAllDistributors = false
      vm.allDistributors = data

  vm.addUserToDistributor = (ev, userEmail, distributorAdmin, whichDistributor, form) ->
    if not distributorAdmin
      distributorAdmin = false
    withOrWithout = if distributorAdmin then "with" else "without"

    # no option to select distributor is given when there is only one option
    if not whichDistributor
      whichDistributor = vm.allDistributors[0]

    confirm = $mdDialog.confirm()
    confirm.title('Are you sure?')
    confirm.textContent("#{userEmail.email} will be added to #{whichDistributor}
      #{withOrWithout} administrator priviledges"
    )
    confirm.ariaLabel('Create a User')
    confirm.targetEvent(ev)
    confirm.ok('Of course!')
    confirm.cancel('Oops, nevermind.')

    $mdDialog.show(confirm).then ->
      addUserToDistributorPromise = AdminService.addUserToDistributor(userEmail.email, whichDistributor, distributorAdmin)
      addUserToDistributorPromise.then (data) ->
        ToastsService.showSuccessToast data.message
        vm.user = {}
        form.$setPristine()
        form.$setUntouched()
        setTimeout (->
          vm.getUsersOfDistributor()
        ), 2000

      addUserToDistributorPromise.catch (data) ->
        ToastsService.showErrorToast data.message

  vm.makeDistributor = (ev, distributorName, adminEmail, form) ->
    confirm = $mdDialog.confirm()
    confirm.title('Are you sure?')
    confirm.textContent("If you proceed, #{distributorName} will be created.")
    confirm.ariaLabel('Lucky day')
    confirm.targetEvent(ev)
    confirm.ok('Yeah!')
    confirm.cancel('Forget it.')
    $mdDialog.show(confirm).then (->
      makeDistributorPromise = AdminService.makeDistributor distributorName, adminEmail
      makeDistributorPromise.then (data) ->
        vm.distributor = {}
        form.$setPristine()
        form.$setUntouched()
        ToastsService.showSuccessToast data.message
        setTimeout (->
          vm.allDistributors = vm.getAllDistributors()
        ), 2000

      makeDistributorPromise.catch (data) ->
        ToastsService.showErrorToast data.message
    )

  vm.getUsersOfDistributor = () ->
    vm.loadingUsersOfDistributor = true
    usersofDistributorPromise = AdminService.getUsersOfDistributor(SessionsService.getCurrentDistributorKey())
    usersofDistributorPromise.then (data) ->
      vm.loadingUsersOfDistributor = false
      vm.usersOfDistributor = data

  vm.switchDistributor = (distributor) ->
    DistributorsService.switchDistributor(distributor)
    ToastsService.showSuccessToast "Distributor #{distributor.name} selected!"

  vm.initialize = () ->
    vm.getUsersOfDistributor()
    vm.getAllDistributors()
    vm.isAdmin = SessionsService.getIsAdmin()
    vm.distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()
    vm.currentDistributorName = SessionsService.getCurrentDistributorName()


    if vm.isAdmin
      vm.getAllDistributors()

  vm
