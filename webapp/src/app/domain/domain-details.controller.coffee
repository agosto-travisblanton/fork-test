'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'DomainDetailsCtrl', ($log,
                                           $stateParams,
                                           DomainsService,
                                           $state,
                                           sweet,
                                           ProgressBarService) ->
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
