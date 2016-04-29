'use strict'

angular.module('skykitProvisioning').factory 'ProgressBarService', (ngProgressFactory) ->
  new class ProgressBarService
    constructor: ->
      @progressBar = ngProgressFactory.createInstance()

    start: ->
      @progressBar.setColor('#00FCFF')
      @progressBar.setHeight('4px')
      @progressBar.start()

    complete: ->
      @progressBar.complete()



