'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'DisplaysService', ($http, $log, Restangular) ->

  class DisplaysService
    SERVICE_NAME = 'displays'
    @uriBase = 'v1/displays'

    getByMacAddress: (macAddress) ->
      Restangular.oneUrl('api/v1/displays', "api/v1/displays?mac_address=#{macAddress}").get()

    getByKey: (displayKey) ->
      promise = Restangular.oneUrl(SERVICE_NAME, "api/v1/displays/#{displayKey}").get()
      promise

    getDisplaysByTenant: (tenantKey) ->
      unless tenantKey == undefined
        promise = Restangular.one('tenants', tenantKey).doGET(SERVICE_NAME)
        promise

    getDisplays: ->
      params = {}
      promise = Restangular.all(SERVICE_NAME).getList()
      promise

    save: (display) ->
      if display.key != undefined
        promise = display.put()
      else
        promise = Restangular.service(SERVICE_NAME).post(display)
      promise


  new DisplaysService()
