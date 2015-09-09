'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DomainDetailsCtrl', ($log,
                                           $stateParams,
                                           DistributorsService,
                                           DomainsService,
                                           $state,
                                           sweet,
                                           ProgressBarService) ->
  @default_distributor = 'Agosto'

  @distributors = []

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

  @initialize = ->
    distributorPromise = DistributorsService.getByName(@default_distributor)
    distributorPromise.then (data) =>
      if typeof data[0] != 'undefined'
        @currentDomain.distributor_key = data[0].key

  @onClickSaveButton = ->
    ProgressBarService.start()
    promise = DomainsService.save @currentDomain
    promise.then @onSuccessDomainSave, @onFailureDomainSave

  @onSuccessDomainSave = ->
    ProgressBarService.complete()
    $state.go 'domains'

  @onFailureDomainSave = (errorObject) ->
    ProgressBarService.complete()
    $log.error errorObject
    sweet.show('Oops...', 'Unable to save the domain.', 'error')

  @editItem = (item) ->
    $state.go 'editDomain', {domainKey: item.key}


  @
