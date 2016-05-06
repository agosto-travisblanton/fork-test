'use strict'

angular.module('skykitProvisioning').factory 'DevicesService', ($log, Restangular, $q, CacheFactory, $http, $cookies) ->
  new class DevicesService

    constructor: ->
      @SERVICE_NAME = 'devices'
      @uriBase = 'v1/devices'
      if !CacheFactory.get('deviceCache')
        distributorKey = $cookies.get('currentDistributorKey')

        @deviceCache = CacheFactory('deviceCache',
          maxAge: 60 * 60 * 1000
          deleteOnExpire: 'aggressive'
          storageMode: 'localStorage'
          onExpire: (key, value) ->
            $http.get(key).success (data) ->
              @deviceCache.put key, data
              return
            return
        )
      if !CacheFactory.get('deviceByTenantCache')
        @deviceByTenantCache = CacheFactory('deviceByTenantCache',
          maxAge: 60 * 60 * 1000
          deleteOnExpire: 'aggressive'
          storageMode: 'localStorage'
          onExpire: (key, value) ->
            $http.get(key).success (data) ->
              @deviceByTenantCache.put key, data
              return
            return
        )

    getDeviceByMacAddress: (macAddress) ->
      url = "api/v1/devices?mac_address=#{macAddress}"
      Restangular.oneUrl('api/v1/devices', url).get()

    getDeviceByKey: (deviceKey) ->
      url = "api/v1/devices/#{deviceKey}"
      promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
      promise

    getIssuesByKey: (deviceKey, startEpoch, endEpoch, prev, next) ->
      prev = if prev == undefined or null then null else prev
      next = if next == undefined or null then null else next
      url = "/api/v1/devices/#{prev}/#{next}/#{deviceKey}/issues?start=#{startEpoch}&end=#{endEpoch}"
      promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
      promise

    getCommandEventsByKey: (deviceKey, prev, next) ->
      prev = if prev == undefined or null then null else prev
      next = if next == undefined or null then null else next
      url = "/api/v1/player-command-events/#{prev}/#{next}/#{deviceKey}"
      promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
      promise

########################################################################
# TENANT VIEW
########################################################################
    getDevicesByTenant: (tenantKey, prev, next) ->
      unless tenantKey == undefined
        deferred = $q.defer()
        url = @makeDevicesByTenantURL tenantKey, prev, next, false
        if not @deviceByTenantCache.get(url)
          promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
          promise.then (data) =>
            @deviceByTenantCache.put url, data
            deferred.resolve(data)
        else
          deferred.resolve(@deviceByTenantCache.get(url))

        deferred.promise

    getUnmanagedDevicesByTenant: (tenantKey, prev, next) ->
      unless tenantKey == undefined
        deferred = $q.defer()
        url = @makeDevicesByTenantURL tenantKey, prev, next, true
        if not @deviceByTenantCache.get(url)
          promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
          promise.then (data) =>
            @deviceByTenantCache.put url, data
            deferred.resolve(data)
        else
          deferred.resolve(@deviceByTenantCache.get(url))

        deferred.promise


    searchDevicesByPartialSerialByTenant: (tenantKey, partial_serial, unmanaged) ->
      unless tenantKey == undefined
        url = "api/v1/tenants/search/serial/#{tenantKey}/#{partial_serial}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    searchDevicesByPartialMacByTenant: (tenantKey, partial_mac, unmanaged) ->
      unless tenantKey == undefined
        url = "api/v1/tenants/search/mac/#{tenantKey}/#{partial_mac}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    matchDevicesByFullSerialByTenant: (tenantKey, full_serial, unmanaged) ->
      unless tenantKey == undefined
        url = "api/v1/tenants/match/serial/#{tenantKey}/#{full_serial}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    matchDevicesByFullMacByTenant: (tenantKey, full_mac, unmanaged) ->
      unless tenantKey == undefined
        url = "api/v1/tenants/match/mac/#{tenantKey}/#{full_mac}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

########################################################################
# DEVICES VIEW
########################################################################
    searchDevicesByPartialSerial: (distributorKey, partial_serial, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/search/serial/#{distributorKey}/#{partial_serial}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    searchDevicesByPartialMac: (distributorKey, partial_mac, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/search/mac/#{distributorKey}/#{partial_mac}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    matchDevicesByFullSerial: (distributorKey, full_serial, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/match/serial/#{distributorKey}/#{full_serial}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    matchDevicesByFullMac: (distributorKey, full_mac, unmanaged) ->
      unless distributorKey == undefined
        url = "api/v1/distributors/match/mac/#{distributorKey}/#{full_mac}/#{unmanaged}/devices"
        promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
        promise

    getDevicesByDistributor: (distributorKey, prev, next) ->
      unless distributorKey == undefined
        deferred = $q.defer()
        url = @makeDevicesByDistributorURL distributorKey, prev, next, false
        if not @deviceCache.get(url)
          promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
          promise.then (data) =>
            @deviceCache.put url, data
            deferred.resolve(data)
        else
          deferred.resolve(@deviceCache.get(url))

        deferred.promise

    getUnmanagedDevicesByDistributor: (distributorKey, prev, next) ->
      unless distributorKey == undefined
        deferred = $q.defer()
        url = @makeDevicesByDistributorURL distributorKey, prev, next, true
        if not @deviceCache.get(url)
          promise = Restangular.oneUrl(@SERVICE_NAME, url).get()
          promise.then (data) =>
            @deviceCache.put url, data
            deferred.resolve(data)
        else
          deferred.resolve(@deviceCache.get(url))

        deferred.promise

    getDevices: ->
      promise = Restangular.all(@SERVICE_NAME).getList()
      promise

    save: (device) ->
      if device.key != undefined
        promise = device.put()
      else
        promise = Restangular.service('devices').post(device)
      promise

    delete: (deviceKey) ->
      promise = Restangular.one(@SERVICE_NAME, deviceKey).remove()
      promise

    getPanelModels: () ->
      [
        {
          'id': 'None'
          'displayName': 'None'
        }
        {
          'id': 'Sony-FXD40LX2F'
          'displayName': 'Sony FXD40LX2F'
        }
        {
          'id': 'NEC-LCD4215'
          'displayName': 'NEC LCD4215'
        }
        {
          'id': 'Phillips-BDL5560EL'
          'displayName': 'Phillips BDL5560EL'
        }
        {
          'id': 'Panasonic-TH55LF6U'
          'displayName': 'Panasonic TH55LF6U'
        }
        {
          'id': 'Sharp-PNE521'
          'displayName': 'Sharp PNE521'
        }
      ]

    getPanelInputs: () ->
      [
        {
          'id': 'None'
          'parentId': 'None'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Sony-FXD40LX2F'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Sony-FXD40LX2F'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'DVI'
          'parentId': 'Phillips-BDL5560EL'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'DVI'
          'parentId': 'Panasonic-TH55LF6U'
        }
        {
          'id': 'HDMI1'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'HDMI2'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'DVI'
          'parentId': 'Sharp-PNE521'
        }
        {
          'id': 'VGA'
          'parentId': 'NEC-LCD4215'
        }
        {
          'id': 'DVI1'
          'parentId': 'NEC-LCD4215'
        }
      ]

    makeDevicesByDistributorURL: (distributorKey, prev, next, unmanaged) ->
      url = "/api/v1/distributors/#{prev}/#{next}/#{distributorKey}/devices?unmanaged=#{unmanaged}"

    makeDevicesByTenantURL: (tenantKey, prev, next, unmanaged) ->
      url = "/api/v1/tenants/#{prev}/#{next}/#{tenantKey}/devices?unmanaged=#{unmanaged}"

