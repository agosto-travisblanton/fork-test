'use strict'

appModule = angular.module('skyKitProvisioning')

appModule.factory 'DomainsService', (Restangular) ->
  new class DomainsService

    save: (domain) ->
      if domain.key != undefined
        promise = domain.put()
      else
        promise = Restangular.service('domains').post(domain)
      promise

    fetchAllDomains: () ->
      promise = Restangular.all('domains').getList()
      promise

    getDomainByKey: (domainKey) ->
      promise = Restangular.oneUrl('domains', "api/v1/domains/#{domainKey}").get()
      promise

    delete: (domain) ->
      if domain.key != undefined
        promise = Restangular.one("domains", domain.key).remove()
        promise
