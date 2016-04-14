'use strict'

angular.module('skykitProvisioning').factory 'ToastsService', (toastr) ->
  new class ToastsService

    showSuccessToast: (message, title = 'Success!') ->
      toastr.success message, title

    showErrorToast: (message, title = 'Error!') ->
      toastr.error message, title

    showInfoToast: (message, title = 'Information') ->
      toastr.info message, title
