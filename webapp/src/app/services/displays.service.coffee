'use strict'

angular.module('skykitDisplayDeviceManagement').factory 'DisplaysService', ($http, $log, Restangular) ->

# TODO: Handle pagination
  class DisplaysService
    @uriBase = 'v1/displays'

    getByMacAddress: (macAddress) ->
      Restangular.oneUrl('api/v1/displays', "api/v1/displays?mac_address=#{macAddress}").get()

    getByKey: (displayKey) ->
      promise = Restangular.oneUrl('displays', "api/v1/displays/#{displayKey}").get()
      promise

    getDisplaysByTenant: (tenantKey) ->
      unless tenantKey == undefined
        promise = Restangular.one('tenants', tenantKey).doGET('displays')
        promise

    getDisplays: ->
      params = {}
      promise = Restangular.all('displays').getList()
      promise

    save: (display) ->
      if display.key != undefined
        promise = display.put()
      else
        promise = Restangular.service('displays').post(display)
      promise


  new DisplaysService()
