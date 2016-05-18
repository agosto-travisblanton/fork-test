'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DomainsCtrl", ($state, $log, DomainsService, sweet) ->
  @domains = []

  @initialize = ->
    promise = DomainsService.fetchAllDomains()
    promise.then (data) =>
      @domains = data

  @editItem = (item) ->
    $state.go 'editDomain', {domainKey: item.key}

  @deleteItem = (item) =>
    callback = () =>
      promise = DomainsService.delete item
      promise.then () =>
        @initialize()
    sweet.show({
      title: "Are you sure?",
      text: "This will permanently remove the domain from the distributor and disconnect from tenants.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, remove the domain!",
      closeOnConfirm: true
    }, callback)


  @
