import naturalSort from 'javascript-natural-sort';


function TenantOverlaysCtrl($stateParams,
                            TenantsService,
                            $state,
                            ProgressBarService,
                            ToastsService,
                            $scope,
                            ImageService,
                            $timeout,
                            $mdDialog) {
  "ngInject";

  let vm = this;
  $scope.tabIndex = 4;
  vm.tenantKey = $stateParams.tenantKey;
  vm.editMode = !!$stateParams.tenantKey;
  vm.currentTenant = null;
  vm.overlayChanged = false;

  ////////////////////////////////////////////////////////////////
  // Overlays
  ////////////////////////////////////////////////////////////////
  vm.adjustOverlayStatus = (status) => {
    vm.currentTenant.overlayStatus = status
    ProgressBarService.start();
    vm.loadingOverlays = true;
    let promise = TenantsService.save(vm.currentTenant);
    promise.then(() => {
      ProgressBarService.complete()
      let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
      tenantPromise.then(function (tenant) {
        vm.loadingOverlays = false;
        return vm.onSuccessResolvingTenant(tenant);
      });
    })
    promise.catch((err) => {
      ProgressBarService.complete();
      ToastsService.showErrorToast('Something went wrong');
      console.log(err)
    })
  }

  vm.updateOverlays = () => {
    vm.loadingOverlays = true;
    let tenantPromise = vm.getTenant();
    tenantPromise.then((tenant) => {
      vm.overlayChanged = false;
      vm.currentTenant.overlays = tenant.overlays;
      vm.currentTenantCopy.overlays = angular.copy(vm.currentTenant.overlays);
      vm.loadingOverlays = false;
    })
    return tenantPromise;
  }

  vm.submitOverlaySettings = () => {
    vm.loadingOverlays = true;

    let overlaySettings = angular.copy(vm.currentTenantCopy.overlays)
    ProgressBarService.start();
    let promise = TenantsService.saveOverlaySettings(
      vm.tenantKey,
      overlaySettings.bottom_left,
      overlaySettings.bottom_right,
      overlaySettings.top_right,
      overlaySettings.top_left
    );

    let updateOverlayPromiseDeferred = () => {
      let updateOverlayPromise = vm.updateOverlays();
      updateOverlayPromise.then((res) => {
        ToastsService.showSuccessToast('We saved your update.');
        ProgressBarService.complete();
      });
    };

    promise.then(() => {
      $timeout(updateOverlayPromiseDeferred, 1000)
    })

    promise.catch((res) => {
      ProgressBarService.complete();
      ToastsService.showErrorToast('Something went wrong');

    })
  };

  vm.applyTenantOverlay = (ev) => {
    let confirm = $mdDialog.confirm(
      {
        title: `Are you sure?`,
        textContent: `Each device in your Tenant will have the current Overlay Template applied as its settings.`,
        targetEvent: ev,
        ariaLabel: 'Lucky day',
        ok: 'Confirm',
        cancel: 'Nevermind'
      }
    );

    $mdDialog.show(confirm).then((function () {
      ProgressBarService.start();
      let promise = TenantsService.overlayApplyTenant(vm.tenantKey)
      promise.then((res) => {
        let message = 'Your Tenant Overlay Settings are being applied to each device in your Tenant. Please wait patiently for this process to complete.'
        ToastsService.showSuccessToast(message);
        vm.loading = true;
        vm.getTenant();
        ProgressBarService.complete()
      })
      promise.catch((res) => {
        ProgressBarService.complete()
        ToastsService.showErrorToast('Something went wrong');

      })
    }))

  }

  vm.checkForOverlayChanges = () => {
    let changed = false;
    let currentTenantOverlays = vm.currentTenant.overlays;
    let currentTenantCopyOverlays = vm.currentTenantCopy.overlays;
    let positions = ['top_left', 'top_right', 'bottom_right', 'bottom_left'];

    for (let pos of positions) {
      if (currentTenantOverlays[pos].size !== currentTenantCopyOverlays[pos].size) {
        changed = true;
      }
      if (currentTenantOverlays[pos].type !== currentTenantCopyOverlays[pos].type) {
        changed = true;
      }
      if (currentTenantOverlays[pos].type === 'logo') {
        if ((currentTenantOverlays[pos].type + ": " + currentTenantOverlays[pos].name) !== currentTenantCopyOverlays[pos].name) {
          changed = true;
        }
      }
    }

    vm.overlayChanged = changed;

  }


  ////////////////////////////////////////////////////////////////
  // Images
  ////////////////////////////////////////////////////////////////
  vm.submitImage = () => {
    if (vm.selectedLogo && vm.selectedLogo[0]) {
      var formData = new FormData();
      let validFile = true;
      angular.forEach(vm.selectedLogo, function (obj) {
        if (obj.lfFile.size < 15000000) {
          formData.append('files', obj.lfFile);
        } else {
          vm.fileApi.removeAll()
          validFile = false;
          ToastsService.showErrorToast('Your image is larger than 15 MB. Please choose a smaller image');
        }
      });

      if (validFile) {
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
  }

  vm.getTenantImagesAndReloadTenantAfterDelete = () => {
    let tenantImagePromise = vm.getTenantImages();
    tenantImagePromise.then(() => {
      let updateOverlayPromise = vm.updateOverlays();
      updateOverlayPromise.then(() => {
        ToastsService.showSuccessToast('We deleted your image.');
        ProgressBarService.complete();
      })
    })
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
          $timeout(vm.getTenantImagesAndReloadTenantAfterDelete, 1000);
        })
        .catch((res) => {
          ToastsService.showErrorToast('Something went wrong while deleting your image.');
          ProgressBarService.complete();
        })
    }))
  };

  vm.getTenantImages = () => {
    vm.OVERLAY_TYPES = [
      {size: null, type: null, name: "none", realName: "none", new: false, image_key: null},
      {size: null, type: "datetime", name: "datetime", realName: "datetime", new: true, image_key: null},
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

    return promise
  };

  //////////////////////////////////////////////////////////////
  // Setup
  //////////////////////////////////////////////////////////////
  vm.onSuccessResolvingTenant = function (tenant) {
    vm.currentTenant = tenant;
    vm.currentTenantCopy = angular.copy(vm.currentTenant);
    vm.selectedTimezone = tenant.default_timezone;

  };

  vm.getTenant = () => {
    let tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey);
    tenantPromise.then(function (tenant) {
      vm.currentTenant = tenant;
      if (vm.currentTenant.overlaysUpdateInProgress) {
        vm.loading = true;
        $timeout(vm.getTenant, 3000);
      } else {
        vm.loading = false;
      }
      vm.currentTenantCopy = angular.copy(vm.currentTenant);
    })
    return tenantPromise
  }

  vm.initialize = () => {
    vm.getTenantImages()
    vm.getTenant()
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
