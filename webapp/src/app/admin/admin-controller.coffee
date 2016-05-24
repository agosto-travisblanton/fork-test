'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService, SessionsService, ToastsService, $mdDialog) ->
  vm = @
  vm.isAdmin = SessionsService.getIsAdmin()
  vm.distributors = SessionsService.getDistributors()
  vm.distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()
  vm.currentDistributorName = SessionsService.getCurrentDistributorName()

  vm.addUserToDistributor = (ev, userEmail, distributorAdmin) ->
    if not distributorAdmin
      distributorAdmin = false
    withOrWithoutString = if distributorAdmin then "with" else "without"
    confirm = $mdDialog.confirm()
    confirm.title('Are you sure?')
    confirm.textContent("#{userEmail.email} will be added to #{vm.currentDistributorName}
      #{withOrWithout} administrator priviledges"
    )
    confirm.ariaLabel('Create a User')
    confirm.targetEvent(ev)
    confirm.ok('Of course!')
    confirm.cancel('Oops, nevermind.')

    $mdDialog.show(confirm).then (->
      res = AdminService.addUserToDistributor(userEmail.email, vm.currentDistributorName, distributorAdmin)
      res.then (data) ->
        ToastsService.showSuccessToast data.data.message
        vm.user = {}
        setTimeout (->
          vm.getUsersOfDistributor()
        ), 1000

      res.catch (data) ->
        ToastsService.showErrorToast data.data.message
    )

  vm.makeDistributor = (ev, distributorName, adminEmail) ->
    confirm = $mdDialog.confirm()
    confirm.title('Are you sure?')
    confirm.textContent("If you proceed, #{distributorName} will be created.")
    confirm.ariaLabel('Lucky day')
    confirm.targetEvent(ev)
    confirm.ok('Yeah!')
    confirm.cancel('Forget it.')
    $mdDialog.show(confirm).then (->
      res = AdminService.makeDistributor distributorName, adminEmail
      res.then (data) ->
        ToastsService.showSuccessToast data.data.message
        setTimeout (->
          vm.getAllDistributors()
        ), 1000

      res.catch (data) ->
        ToastsService.showErrorToast data.data.message
    )

  vm.getUsersOfDistributor = () ->
    vm.loadingUsersOfDistributor = true
    u = AdminService.getUsersOfDistributor(SessionsService.getCurrentDistributorKey())
    u.then (data) ->
      vm.loadingUsersOfDistributor = false
      vm.usersOfDistributor = data.data


  vm.getAllDistributors = () ->
    vm.loadingAllDistributors = true
    d = AdminService.getAllDistributors()
    d.then (data) ->
      vm.loadedData = data.data
      vm.loadingAllDistributors = false
      vm.allDistributors = (each.name for each in vm.loadedData)

  vm.initilize = () ->
    vm.getUsersOfDistributor()

    if vm.isAdmin
      vm.getAllDistributors()

  vm.initilize()
  
  vm
