(function () {

  let appModule = angular.module('skykitProvisioning');

  appModule.controller("DomainsCtrl", function ($state, $log, DomainsService, sweet) {
    let vm = this;
    vm.domains = [];

    vm.initialize = function () {
      let promise = DomainsService.fetchAllDomains();
      return promise.then(data => vm.domains = data);
    };

    vm.editItem = item => $state.go('editDomain', {domainKey: item.key});

    vm.deleteItem = function (item) {
      let callback = function () {
        let promise = DomainsService.delete(item);
        return promise.then(() => vm.initialize());
      };
      return sweet.show({
        title: "Are you sure?",
        text: "This will permanently remove the domain from the distributor and disconnect from tenants.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, remove the domain!",
        closeOnConfirm: true
      }, callback);
    };

    return vm;
  });
})
();
