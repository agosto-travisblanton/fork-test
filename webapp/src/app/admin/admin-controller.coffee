'use strict'

app = angular.module 'skykitProvisioning'

app.controller "AdminCtrl", (AdminService, SessionsService, ToastsService, $mdDialog) ->
  @isAdmin = SessionsService.getIsAdmin()
  console.log @isAdmin
  @distributors = SessionsService.getDistributors()
  @distributorsAsAdmin = SessionsService.getDistributorsAsAdmin()
  console.log @distributorsAsAdmin
  @currentDistributorName = SessionsService.getCurrentDistributerName()

  @addUserToDistributor = (ev, userEmail, distributorAdmin) =>
    if not distributorAdmin
      distributorAdmin = false
    withOrWithout = if distributorAdmin then "with" else "without"
    confirm = $mdDialog.confirm()
    confirm.title('Are you sure?')
    confirm.textContent("#{userEmail.email} will be added to #{@currentDistributorName}
      #{withOrWithout} administrator priviledges"
    )
    confirm.ariaLabel('Create a User')
    confirm.targetEvent(ev)
    confirm.ok('Of course!')
    confirm.cancel('Oops, nevermind.')

    $mdDialog.show(confirm).then (=>
      res = AdminService.addUserToDistributor(userEmail.email, @currentDistributorName, distributorAdmin)
      res.then (data) =>
        ToastsService.showSuccessToast data.data.message
        @user = {}
      res.catch (data) =>
        ToastsService.showErrorToast data.data.message
    )

  @makeDistributor = (ev, distributorName, adminEmail) =>
    confirm = $mdDialog.confirm()
    confirm.title('Are you sure?')
    confirm.textContent("If you proceed, #{distributorName} will be created.")
    confirm.ariaLabel('Lucky day')
    confirm.targetEvent(ev)
    confirm.ok('Yeah!')
    confirm.cancel('Forget it.')
    $mdDialog.show(confirm).then (=>
      res = AdminService.makeDistributor distributorName, adminEmail
      res.then (data) =>
        ToastsService.showSuccessToast data.data.message

      res.catch (data) =>
        ToastsService.showErrorToast data.data.message
    )

  @getUsersOfDistributer = () =>
    @loadingUsersOfDistributer = true
    u = AdminService.getUsersOfDistributor(SessionsService.getCurrentDistributerKey())
    u.then (data) =>
      @loadingUsersOfDistributer = false
      @usersOfDistributer = data.data

  @getUsersOfDistributer()


  @
