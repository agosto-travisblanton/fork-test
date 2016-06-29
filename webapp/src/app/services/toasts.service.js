angular.module('skykitProvisioning').factory('ToastsService', toastr =>
    new class ToastsService {
        constructor() {
        }

        showSuccessToast(message, title = 'Success!') {
            return toastr.success(message, title);
        }

        showErrorToast(message, title = 'Error!') {
            return toastr.error(message, title);
        }

        showInfoToast(message, title = 'Information') {
            return toastr.info(message, title);
        }
    }()
);
