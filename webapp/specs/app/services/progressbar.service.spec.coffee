'use strict'

describe 'ProgressBarService', ->
  ProgressBarService = undefined
  ngProgressFactory = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_ProgressBarService_, _ngProgressFactory_) ->
    ProgressBarService = _ProgressBarService_
    ngProgressFactory = _ngProgressFactory_


  describe 'constructor', ->
    it 'creates an instance of progress bar', ->
      expect(ProgressBarService.progressBar).toBeDefined()


  describe '.start', ->
    it 'sets the progress bar\'s color', ->
      spyOn(ProgressBarService.progressBar, 'setColor').and.callThrough()
      ProgressBarService.start()
      expect(ProgressBarService.progressBar.setColor).toHaveBeenCalledWith '#00FCFF'

    it 'sets the progress bar\'s height', ->
      spyOn(ProgressBarService.progressBar, 'setHeight').and.callThrough()
      ProgressBarService.start()
      expect(ProgressBarService.progressBar.setHeight).toHaveBeenCalledWith '4px'

    it 'starts the progress bar animation', ->
      spyOn(ProgressBarService.progressBar, 'start').and.callThrough()
      ProgressBarService.start()
      expect(ProgressBarService.progressBar.start).toHaveBeenCalled()


  describe '.complete', ->
    it 'complete the progress bar animation', ->
      spyOn(ProgressBarService.progressBar, 'complete').and.callThrough()
      ProgressBarService.complete()
      expect(ProgressBarService.progressBar.complete).toHaveBeenCalled()
