'use strict'

angular.module('skykitProvisioning').factory 'StorageService', () ->
  new class StorageService

    constructor: ->

    set: (key, value) ->
      Lockr.set(key, value)

    get: (key) ->
      Lockr.get(key)
      
    rm: (key) ->
      Lockr.rm(key)

    removeAll: () ->
      Lockr.flush()

