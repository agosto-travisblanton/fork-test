'use strict'

describe 'ToastsService', ->
  beforeEach module 'skykitProvisioning'

  ToastsService = undefined
  toastr = undefined

  beforeEach inject (_ToastsService_, _toastr_) ->
    ToastsService = _ToastsService_
    toastr = _toastr_

  describe '.showSuccessToast', ->
    expectedMessage = 'expected message!'
    expectedTitle = 'Success!'

    beforeEach ->
      spyOn(toastr, 'success')

    it 'defers to toastr.success', ->
      ToastsService.showSuccessToast expectedMessage
      expect(toastr.success).toHaveBeenCalledWith expectedMessage, expectedTitle

    it 'defers to toastr.success with overridden title', ->
      expectedTitle = 'Hey!'
      ToastsService.showSuccessToast expectedMessage, expectedTitle
      expect(toastr.success).toHaveBeenCalledWith expectedMessage, expectedTitle

  describe '.showErrorToast', ->
    expectedMessage = 'expected message!'
    expectedTitle = 'Error!'

    beforeEach ->
      spyOn(toastr, 'error')

    it 'defers to toastr.error', ->
      ToastsService.showErrorToast expectedMessage
      expect(toastr.error).toHaveBeenCalledWith expectedMessage, expectedTitle

    it 'defers to toastr.error with overridden title', ->
      expectedTitle = 'Hey!'
      ToastsService.showErrorToast expectedMessage, expectedTitle
      expect(toastr.error).toHaveBeenCalledWith expectedMessage, expectedTitle

  describe '.showInfoToast', ->
    expectedMessage = 'expected message!'
    expectedTitle = 'Information'

    beforeEach ->
      spyOn(toastr, 'info')

    it 'defers to toastr.info', ->
      ToastsService.showInfoToast expectedMessage
      expect(toastr.info).toHaveBeenCalledWith expectedMessage, expectedTitle

    it 'defers to toastr.info with overridden title', ->
      expectedTitle = 'Hey!'
      ToastsService.showInfoToast expectedMessage, expectedTitle
      expect(toastr.info).toHaveBeenCalledWith expectedMessage, expectedTitle
