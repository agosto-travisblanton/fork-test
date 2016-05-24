'use strict'

appModule = angular.module 'skykitProvisioning'

appModule.controller "DomainsCtrl", ($state, $log, DomainsService, sweet) ->
  vm = @
  vm.domains = []

  vm.initialize = ->
    promise = DomainsService.fetchAllDomains()
    promise.then (data) ->
      vm.domains = data

  vm.editItem = (item) ->
    $state.go 'editDomain', {domainKey: item.key}

  vm.deleteItem = (item) ->
    callback = () ->
      promise = DomainsService.delete item
      promise.then () ->
        vm.initialize()
    sweet.show({
      title: "Are you sure?",
      text: "This will permanently remove the domain from the distributor and disconnect from tenants.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, remove the domain!",
      closeOnConfirm: true
    }, callback)

  vm
