(function () {


  let appModule = angular.module('skykitProvisioning');
  appModule.controller("ProofOfPlayMultiLocationCtrl", function (ProofPlayService, $stateParams, $state, ToastsService) {
    let vm = this;
    vm.radioButtonChoices = {
      group1: 'By Device',
      group2: 'Summarized',
      selection: null
    };


    vm.dateTimeSelection = {
      start: null,
      end: null
    };

    vm.formValidity = {
      start_date: false,
      end_date: false,
      locations: false,
    };

    vm.tenant = $stateParams.tenant;
    vm.no_cache = true;
    vm.loading = true;
    vm.disabled = true;
    vm.disabledTenant = true;
    vm.selected_locations = [];

    vm.initialize = () =>
      ProofPlayService.getAllLocations(vm.tenant)
        .then(function (data) {
          vm.loading = false;
          vm.locations = data.data.locations;
          if (vm.locations.length > 0) {
            return vm.had_some_items = true;
          } else {
            return vm.had_some_items = false;
          }
        })
    ;

    vm.refreshLocations = function () {
      vm.searchText = '';
      vm.selectedItem = '';
      vm.loading = true;
      vm.disabled = true;
      vm.selected_locations = [];
      return vm.initialize();
    };

    vm.addToSelectedLocations = function (searchText) {
      if (vm.isLocationValid(searchText)) {
        vm.selected_locations.push(searchText);
        let index = vm.locations.indexOf(searchText);
        vm.locations.splice(index, 1);
        vm.searchText = '';
      }
      vm.areLocationsValid();
      return vm.isDisabled();
    };

    vm.querySearch = (locations, searchText) => ProofPlayService.querySearch(locations, searchText);


    vm.isRadioValid = function (selection) {
      vm.formValidity.type = selection;
      return vm.isDisabled();
    };


    vm.isLocationValid = function (searchText) {
      if (__in__(searchText, vm.locations)) {
        if (!__in__(searchText, vm.selected_locations)) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    };


    vm.areLocationsValid = function () {
      vm.formValidity.locations = (vm.selected_locations.length > 0);
      return vm.isDisabled();
    };

    vm.isStartDateValid = function (start_date) {
      vm.formValidity.start_date = (start_date instanceof Date);
      return vm.isDisabled();
    };


    vm.isEndDateValid = function (end_date) {
      vm.formValidity.end_date = (end_date instanceof Date);
      return vm.isDisabled();
    };

    vm.removeFromSelectedLocation = function (item) {
      let index = vm.selected_locations.indexOf(item);
      vm.selected_locations.splice(index, 1);
      vm.locations.push(item);
      vm.areLocationsValid();
      return vm.isDisabled();
    };


    vm.isDisabled = function () {
      if (vm.formValidity.start_date && vm.formValidity.end_date && vm.formValidity.locations && vm.formValidity.type) {
        vm.disabled = false;
        return vm.final = {
          start_date_unix: moment(vm.dateTimeSelection.start).unix(),
          end_date_unix: moment(vm.dateTimeSelection.end).unix(),
          locations: vm.selected_locations,
          type: vm.radioButtonChoices.selection

        };

      } else {
        return vm.disabled = true;
      }
    };

    vm.submit = function () {
      if (vm.final.type === "1") {
        return ProofPlayService.downloadCSVForMultipleLocationsByDevice(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.locations, vm.tenant);

      } else {
        return ProofPlayService.downloadCSVForMultipleLocationsSummarized(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.locations, vm.tenant);
      }
    };

    vm.tenants = null;
    vm.currentTenant = vm.tenant;

    vm.initialize_tenant_select = () =>
      ProofPlayService.getAllTenants()
        .then(data => vm.tenants = data.data.tenants)
    ;

    vm.querySearch = (resources, searchText) => ProofPlayService.querySearch(resources, searchText);

    vm.isSelectionValid = function (search) {
      if (__in__(search, vm.tenants)) {
        return vm.disabledTenant = false;
      } else {
        return vm.disabledTenant = true;
      }
    };


    vm.submitTenant = function (tenant) {
      if (tenant !== vm.currentTenant) {
        $state.go('proofDetail', {
          tenant
        });

        return ToastsService.showSuccessToast(`Proof of Play reporting set to ${tenant}`);

      } else {
        return ToastsService.showErrorToast(`Proof of Play reporting is already set to ${tenant}`);
      }
    };

    return vm;
  });
  function __in__(needle, haystack) {
    return haystack.indexOf(needle) >= 0;
  }

})
();
