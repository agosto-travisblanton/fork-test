'use strict'

angular.module('skykitProvisioning').factory 'TimezonesService', ($http, $log, Restangular) ->
  class TimezonesService

    getUsTimezones: () ->
      promise = Restangular.oneUrl('timezones', 'api/v1/timezones/us').get()
      promise

    getAllTimezones: () ->
      promise = Restangular.oneUrl('timezones', 'api/v1/timezones/all').get()
      promise

  new TimezonesService()
