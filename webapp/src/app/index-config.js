(function () {

    let app = angular.module('skykitProvisioning');

    app.config(toastrConfig =>
        angular.extend(toastrConfig, {
            progressBar: true,
            closeButton: true,
            tapToDismiss: true,
            newestOnTop: true,
            positionClass: 'toast-bottom-left',
            timeOut: 5000
        })
    );

    app.config($breadcrumbProvider =>
        $breadcrumbProvider.setOptions({
            prefixStateName: 'home',
            template: 'bootstrap3'
        })
    );

})
();