import angular from 'angular';

export function addRequestInterceptor($httpProvider) {
  $httpProvider.interceptors.push('RequestInterceptor');
}
addRequestInterceptor.$inject = ['$httpProvider'];


export function toastrConfig(toastrConfig) {
  angular.extend(toastrConfig, {
    progressBar: true,
    closeButton: true,
    tapToDismiss: true,
    newestOnTop: true,
    positionClass: 'toast-bottom-left',
    timeOut: 5000
  })
}
toastrConfig.$inject = ['toastrConfig'];


export function breadcrumbProvider($breadcrumbProvider) {
  $breadcrumbProvider.setOptions({
    prefixStateName: 'home',
    template: 'bootstrap3'
  })
}

breadcrumbProvider.$inject = ["$breadcrumbProvider"]


