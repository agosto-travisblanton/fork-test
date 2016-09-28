import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject
let controller = undefined;


describe('TenantOverlaysCtrl', function () {
  let scope = undefined;
  let tenantsServicePromiseSave = undefined;
  let $timeout = undefined;
  let $controller = undefined;
  let $state = undefined;
  let $stateParams = undefined;
  let TenantsService = undefined;
  let DevicesService = undefined;
  let serviceInjection = undefined;
  let tenantsServicePromise = undefined;
  let promise = undefined;
  let ProgressBarService = undefined;
  let imageServicePromise = undefined;
  let partial = undefined;
  let $q = undefined;
  let ImageService = undefined;
  let tenantsSaveOverlayPromise = undefined;
  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_$controller_,
                              _$timeout_,
                              _$q_,
                              _TenantsService_,
                              _DevicesService_,
                              _ProgressBarService_,
                              _ImageService_,
                              _$state_,
                              _$rootScope_) {
    $controller = _$controller_;
    $state = _$state_;
    $stateParams = {};
    let $rootScope = _$rootScope_;
    ImageService = _ImageService_;
    TenantsService = _TenantsService_;
    DevicesService = _DevicesService_;
    ProgressBarService = _ProgressBarService_;
    $timeout = _$timeout_;
    scope = $rootScope.$new();
    serviceInjection = {
      ImageService: ImageService,
      $scope: scope,
      $stateParams,
      TenantsService,
      DevicesService,
      ProgressBarService
    };
    $q = _$q_;
    controller = $controller('TenantOverlaysCtrl', serviceInjection);

  }));

  describe('TenantOverlaysCtrl', function () {
    beforeEach(function () {
      tenantsSaveOverlayPromise = new skykitProvisioning.q.Mock();
      tenantsServicePromiseSave = new skykitProvisioning.q.Mock();

      tenantsServicePromise = new skykitProvisioning.q.Mock();
      imageServicePromise = new skykitProvisioning.q.Mock();
      spyOn(ImageService, 'deleteImage').and.returnValue(imageServicePromise);
      spyOn(ImageService, 'saveImage').and.returnValue(imageServicePromise);
      spyOn(ImageService, 'getImages').and.returnValue(imageServicePromise);
      spyOn(ProgressBarService, 'start');
      spyOn(ProgressBarService, 'complete');
      spyOn(TenantsService, 'saveOverlaySettings').and.returnValue(tenantsSaveOverlayPromise)
      spyOn(TenantsService, 'overlayApplyTenant').and.returnValue(tenantsServicePromise);
      spyOn(TenantsService, 'save').and.returnValue(tenantsServicePromiseSave);
      spyOn(TenantsService, 'getTenantByKey').and.returnValue(tenantsServicePromise);
      controller.currentTenantCopy = {};
      controller.currentTenant = {};
    });

    describe('adjustOverlayStatus', function () {

      it('saves then gets tenant', function () {
        controller.adjustOverlayStatus(true)
        expect(controller.loadingOverlays).toEqual(true);

        tenantsServicePromiseSave.resolve(true)
        tenantsServicePromise.resolve(true)
        expect(controller.loadingOverlays).toEqual(false);

        // expect(TenantsService, 'getTenantByKey').toHaveBeenCalled();
        // expect(TenantsService, 'save').toHaveBeenCalled();
      })
    });


    describe('updateOverlays', function () {
      it('hides then updates overlays', function () {
        controller.updateOverlays(true)
        expect(controller.loadingOverlays).toBe(true)
        let overlays = 'something'
        tenantsServicePromise.resolve({overlays: overlays})
        expect(controller.loadingOverlays).toBe(false)
        expect(controller.currentTenant.overlays).toEqual(overlays)
      })
    });

    // Todo: Fix this test. fails with:
    `TypeError: undefined is not a constructor (evaluating 'this.resolveFunc(args)') in /Users/danielternyak/agosto/skykit-display-device/webapp/spec.bundle.specific.js (line 113)
    There's some kind of bug in spec.bundle.js window.skykitProvisioning.q.Mock 
    I have spent many hours looking at what the problem is in there to no avail.
    You'll probably want to stop using it entirely, but most of the codebase is current using it`
    // describe('submitOverlaySettings', function () {
    //   it('hides then updates overlays', function () {
    //     controller.currentTenant = {}
    //     controller.currentTenant.overlays = {
    //       top_left: {},
    //       bottom_left: {},
    //       top_right: {},
    //       bottom_right: {}
    //     }
    //     controller.currentTenantCopy = angular.copy(controller.currentTenant);
    //     controller.submitOverlaySettings(true)
    //     expect(controller.loadingOverlays).toEqual(true)
    //     tenantsSaveOverlayPromise.resolve()
    //     tenantsServicePromise.resolve();
    //     expect(controller.loadingOverlays).toEqual(false)
    //
    //     $timeout.flush();
    //   })
    // });

    describe('checkForOverlayChanges', function () {

      it('overlayChanged reflects change value of false when unchanged', function () {
        controller.currentTenant = {}
        controller.currentTenant.overlays = {
          top_left: {},
          bottom_left: {},
          top_right: {},
          bottom_right: {}
        }
        controller.currentTenantCopy = angular.copy(controller.currentTenant);
        controller.checkForOverlayChanges()
        expect(controller.overlayChanged).toEqual(false)

      })


      it('overlayChanged reflects change value of true when unchanged', function () {
        controller.currentTenant = {}
        controller.currentTenant.overlays = {
          top_left: {size: "small"},
          bottom_left: {},
          top_right: {},
          bottom_right: {}
        }
        controller.currentTenantCopy = angular.copy(controller.currentTenant);
        controller.currentTenantCopy.overlays.top_left = {size: "large"}
        controller.checkForOverlayChanges()
        expect(controller.overlayChanged).toEqual(true)

      })
    });


  });
})
;
