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
  StorageService) ->
    @currentDomain = {
      key: undefined,
      name: undefined,
      impersonation_admin_email_address: undefined,
      distributor_key: undefined,
      active: true
    }
    @currentDomains = []
    @editMode = !!$stateParams.domainKey

    if @editMode
      domainPromise = DomainsService.getDomainByKey($stateParams.domainKey)
      domainPromise.then (data) =>
        @currentDomain = data
    else
      @currentDomain.distributor_key = StorageService.get('currentDistributorKey')

    @onSaveDomain = ->
      ProgressBarService.start()
      promise = DomainsService.save @currentDomain
      promise.then @onSuccessSaveDomain, @onFailureSaveDomain

    @onSuccessSaveDomain = ->
      ProgressBarService.complete()
      ToastsService.showSuccessToast 'We saved your update.'

    @onFailureSaveDomain = (error) ->
      ProgressBarService.complete()
      if error.status == 409
        $log.info( "Failure saving domain. Domain already exists: #{error.status} #{error.statusText}")
        sweet.show('Oops...', 'This domain name already exist. Please enter a unique domain name.', 'error')
      else
        $log.error "Failure saving domain: #{error.status } #{error.statusText}"
        ToastsService.showErrorToast 'Oops. We were unable to save your updates at this time.'

    @editItem = (item) ->
      $state.go 'editDomain', {domainKey: item.key}


    @
