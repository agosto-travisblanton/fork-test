'use strict'

appModule = angular.module 'skykitDisplayDeviceManagement'

appModule.controller "DomainsCtrl", ($state, $log, DomainsService, sweet) ->
  @domains = []

  @initialize = ->
    promise = DomainsService.fetchAllDomains()
    promise.then (data) =>
      @domains = data

  @
