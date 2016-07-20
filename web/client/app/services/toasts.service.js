export default class ToastsService {
  constructor(toastr) {
    this.toastr = toastr
  }

  showSuccessToast(message, title = 'Success!') {
    return this.toastr.success(message, title);
  }

  showErrorToast(message, title = 'Error!') {
    return this.toastr.error(message, title);
  }

  showInfoToast(message, title = 'Information') {
    return this.toastr.info(message, title);
  }

  static toastsServiceFactory(toastr) {
    return new ToastsService(toastr)
  }
}

ToastsService.toastsServiceFactory.$inject = [
  "toastr"
]
