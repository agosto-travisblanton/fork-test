import naturalSort from 'javascript-natural-sort';


function TenantOverlaysCtrl($stateParams,
                            TenantsService,
                            DomainsService,
                            TimezonesService,
                            DistributorsService,
                            $state,
                            sweet,
                            ProgressBarService,
                            ToastsService,
                            SessionsService,
                            $scope,
                            $location,
                            ImageService,
                            $timeout,
                            $mdDialog) {
  "ngInject";

  let vm = this;

  $scope.tabIndex = 4;
  vm.tenantKey = $stateParams.tenantKey;
  vm.editMode = !!$stateParams.tenantKey;
  vm.currentTenant = null;

  ////////////////////////////////////////////////////////////////
  // Overlays
  ////////////////////////////////////////////////////////////////
  vm.adjustOverlayStatus = (status) => {
    vm.currentTenant.overlayStatus = status
    ProgressBarService.start();
    let promise = TenantsService.save(vm.currentTenant);
    promise.then(() => {
      ProgressBarService.complete()
      let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
      tenantPromise.then(function (tenant) {
        return vm.onSuccessResolvingTenant(tenant);
      });
    })
    promise.catch((err) => {
      ProgressBarService.complete();
      console.log(err)
    })
  }

  vm.submitOverlaySettings = () => {
    let overlaySettings = angular.copy(vm.currentTenantCopy.overlays)
    delete overlaySettings.key;
    delete overlaySettings.device_key;

    let overlaySettingsCopy = {}
    for (let k in overlaySettings) {
      if (typeof overlaySettings[k] === 'string' || overlaySettings[k] instanceof String) {
        overlaySettingsCopy[k] = JSON.parse(overlaySettings[k])
      } else {
        overlaySettingsCopy[k] = overlaySettings[k]
      }
    }

    ProgressBarService.start();
    let promise = TenantsService.saveOverlaySettings(
      vm.tenantKey,
      overlaySettingsCopy.bottom_left,
      overlaySettingsCopy.bottom_right,
      overlaySettingsCopy.top_right,
      overlaySettingsCopy.top_left
    )
    promise.then((res) => {
      ProgressBarService.complete();
      ToastsService.showSuccessToast('We saved your update.');
    })

    promise.catch((res) => {
      ProgressBarService.complete();
      ToastsService.showErrorToast('Something went wrong');

    })
  };


  ////////////////////////////////////////////////////////////////
  // Images
  ////////////////////////////////////////////////////////////////
  vm.submitImage = () => {
    if (vm.selectedLogo && vm.selectedLogo[0]) {
      var formData = new FormData();
      angular.forEach(vm.selectedLogo, function (obj) {
        formData.append('files', obj.lfFile);
      });

      let promise = ImageService.saveImage(vm.tenantKey, formData)
      promise.then((res) => {
        ProgressBarService.complete();
        $timeout(vm.getTenantImages, 1000);
        vm.fileApi.removeAll()
        ToastsService.showSuccessToast('We uploaded your image.');
      })
      promise.catch((res) => {
        ProgressBarService.complete();
        ToastsService.showErrorToast('Something went wrong. You may have already uploaded this image.');
      })
    }
  }

  vm.deleteImage = (ev, name, key) => {
    let confirm = $mdDialog.confirm(
      {
        title: `Are you sure?`,
        textContent: `If you proceed, ${name} will be deleted and removed from all devices that use it.`,
        targetEvent: ev,
        ariaLabel: 'Lucky day',
        ok: 'Confirm',
        cancel: 'Nevermind'
      }
    );

    $mdDialog.show(confirm).then((function () {
      ProgressBarService.start();

      ImageService.deleteImage(key)
        .then((res) => {
          $timeout(vm.getTenantImages, 1000);
          ToastsService.showSuccessToast('We deleted your image.');
          ProgressBarService.complete();
        })
        .catch((res) => {
          $timeout(vm.getTenantImages, 1000);
          ToastsService.showErrorToast('Something went wrong while deleting your image.');

          ProgressBarService.complete();
        })
    }))
  };

  vm.getTenantImages = () => {
    vm.OVERLAY_TYPES = [
      {size: null, type: null, name: "none", realName: "none", new: false, image_key: null},
      {size: null, type: "datetime", name: "datetime", realName: "datetime", new: true, image_key: null},
      // {size: "large", type: "datetime", name: "datetime", realName: "datetime", new: true, image_key: null},
      // {size: "default", type: "datetime", name: "datetime", realName: "datetime", new: true, image_key: null},
    ]

    ProgressBarService.start();
    let promise = ImageService.getImages(vm.tenantKey);
    promise.then((res) => {
      vm.tenantImages = res
      ProgressBarService.complete();
      for (let value of vm.tenantImages) {
        for (let sizeOption of ["small", "large"]) {
          let newValue = {
            realName: angular.copy(value.name),
            name: "logo: " + value.name,
            type: "logo",
            size: sizeOption,
            image_key: value.key
          }
          vm.OVERLAY_TYPES.push(newValue);
        }
      }
      vm.OVERLAY_TYPES.sort(naturalSort);

    });

    promise.catch(() => {
      ProgressBarService.complete();
      ToastsService.showErrorStatus("SOMETHING WENT WRONG RETRIEVING YOUR IMAGES")
    })
  };

  //////////////////////////////////////////////////////////////
  // Setup
  //////////////////////////////////////////////////////////////
  vm.onSuccessResolvingTenant = function (tenant) {
    vm.currentTenant = tenant;
    vm.currentTenantCopy = angular.copy(vm.currentTenant);
    vm.selectedTimezone = tenant.default_timezone;
    let domainPromise = DomainsService.getDomainByKey(tenant.domain_key);
    return domainPromise.then(data => vm.selectedDomain = data);
  };

  vm.initialize = () => {
    vm.getTenantImages()
    let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
    tenantPromise.then(function (tenant) {
      vm.currentTenant = tenant;
      vm.currentTenantCopy = angular.copy(vm.currentTenant);
      return vm.onSuccessResolvingTenant(tenant);
    });
  }


  $scope.$watch('tabIndex', function (toTab, fromTab) {
    if (toTab !== undefined) {
      switch (toTab) {
        case 0:
          return $state.go('tenantDetails', {tenantKey: $stateParams.tenantKey});
        case 1:
          return $state.go('tenantManagedDevices', {tenantKey: $stateParams.tenantKey});
        case 2:
          return $state.go('tenantUnmanagedDevices', {tenantKey: $stateParams.tenantKey});
        case 3:
          return $state.go('tenantLocations', {tenantKey: $stateParams.tenantKey});
        case 4:
          return $state.go('tenantOverlays', {tenantKey: $stateParams.tenantKey});
      }
    }
  });

  return vm;
}

export {TenantOverlaysCtrl}
