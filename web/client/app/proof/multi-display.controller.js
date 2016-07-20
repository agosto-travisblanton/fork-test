function ProofOfPlayMultiDisplayCtrl(ProofPlayService, $stateParams, $state, ToastsService) {
  let vm = this;

  vm.radioButtonChoices = {
    group1: 'By Date',
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
    displays: false,
  };

  vm.tenant = $stateParams.tenant;
  vm.no_cache = true;
  vm.loading = true;
  vm.disabled = true;
  vm.disabledTenant = true;
  vm.selected_displays = [];


  vm.initialize = () =>
    ProofPlayService.getAllDisplays(vm.tenant)
      .then(function (data) {
        vm.loading = false;
        vm.displays = data.data.devices;
        if (vm.displays.length > 0) {
          return vm.had_some_items = true;
        } else {
          return vm.had_some_items = false;
        }
      })
  ;

  vm.refreshDisplays = function () {
    vm.searchText = '';
    vm.selectedItem = '';
    vm.loading = true;
    vm.disabled = true;
    vm.selected_displays = [];
    ProofPlayService.proofplayCache.removeAll();
    return vm.initialize();
  };

  vm.addToSelectedDisplays = function (searchText) {
    if (vm.isDisplayValid(searchText)) {
      vm.selected_displays.push(searchText);
      let index = vm.displays.indexOf(searchText);
      vm.displays.splice(index, 1);
      vm.searchText = '';
    }
    vm.areDisplaysValid();
    return vm.isDisabled();
  };

  vm.querySearch = (displays, searchText) => ProofPlayService.querySearch(displays, searchText);


  vm.isRadioValid = function (selection) {
    vm.formValidity.type = selection;
    return vm.isDisabled();
  };


  vm.isDisplayValid = function (searchText) {
    if (__in__(searchText, vm.displays)) {
      if (!__in__(searchText, vm.selected_displays)) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  };

  vm.areDisplaysValid = function () {
    vm.formValidity.displays = (vm.selected_displays.length > 0);
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

  vm.removeFromSelectedDisplay = function (item) {
    let index = vm.selected_displays.indexOf(item);
    vm.selected_displays.splice(index, 1);
    vm.displays.push(item);
    vm.areDisplaysValid();
    return vm.isDisabled();
  };


  vm.isDisabled = function () {
    if (vm.formValidity.start_date && vm.formValidity.end_date && vm.formValidity.displays && vm.formValidity.type) {
      vm.disabled = false;
      return vm.final = {
        start_date_unix: moment(vm.dateTimeSelection.start).unix(),
        end_date_unix: moment(vm.dateTimeSelection.end).unix(),
        displays: vm.selected_displays,
        type: vm.radioButtonChoices.selection

      };

    } else {
      return vm.disabled = true;
    }
  };

  vm.submit = function () {
    if (vm.final.type === "1") {
      return ProofPlayService.downloadCSVForMultipleDevicesByDate(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.displays, vm.tenant);

    } else {
      return ProofPlayService.downloadCSVForMultipleDevicesSummarized(vm.final.start_date_unix, vm.final.end_date_unix, vm.final.displays, vm.tenant);
    }
  };


  vm.tenants = null;
  vm.currentTenant = vm.tenant;

  vm.initialize_tenant_select = () =>
    ProofPlayService.getAllTenants()
      .then(data => vm.tenants = data.data.tenants)
  ;

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

  vm.querySearch = (resources, searchText) => ProofPlayService.querySearch(resources, searchText);

  vm.isSelectionValid = function (search) {
    if (__in__(search, vm.tenants)) {
      return vm.disabledTenant = false;
    } else {
      return vm.disabledTenant = true;
    }
  };


  return vm;
};

function __in__(needle, haystack) {
  return haystack.indexOf(needle) >= 0;
}

export {ProofOfPlayMultiDisplayCtrl}
