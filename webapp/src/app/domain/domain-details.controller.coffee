'use strict'
appModule = angular.module('skykitProvisioning')
appModule.controller 'DomainDetailsCtrl', ($log,
  $stateParams,
  DistributorsService,
  DomainsService,
  $state,
  sweet,
  ProgressBarService,
  ToastsService,
  SessionsService) ->
  vm = @
  vm.currentDomain = {
    key: undefined,
    name: undefined,
    impersonation_admin_email_address: undefined,
    distributor_key: undefined,
    active: true
  }
  vm.currentDomains = []
  vm.editMode = !!$stateParams.domainKey

  if vm.editMode
    domainPromise = DomainsService.getDomainByKey($stateParams.domainKey)
    domainPromise.then (data) ->
      vm.currentDomain = data
  else
    vm.currentDomain.distributor_key = SessionsService.getCurrentDistributorKey()

  vm.onSaveDomain = ->
    ProgressBarService.start()
    promise = DomainsService.save vm.currentDomain
    promise.then vm.onSuccessSaveDomain, vm.onFailureSaveDomain

  vm.onSuccessSaveDomain = ->
    ProgressBarService.complete()
    ToastsService.showSuccessToast 'We saved your update.'

  vm.onFailureSaveDomain = (error) ->
    ProgressBarService.complete()
    if error.status == 409
      $log.info("Failure saving domain. Domain already exists: #{error.status} #{error.statusText}")
      sweet.show('Oops...', 'This domain name already exist. Please enter a unique domain name.', 'error')
    else
      $log.error "Failure saving domain: #{error.status } #{error.statusText}"
      ToastsService.showErrorToast 'Oops. We were unable to save your updates at this time.'

  vm.editItem = (item) ->
    $state.go 'editDomain', {domainKey: item.key}


  vm
