(function () {


  let appModule = angular.module('skykitProvisioning');

  appModule.controller("DistributorsCtrl", function ($state) {
    let vm = this;
    vm.distributors = [];

    return vm;
  });
})
();
