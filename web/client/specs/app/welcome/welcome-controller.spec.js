import angular from 'angular';

import VersionsServiceFactory from './../../../app/services/versions.service'
import StorageServiceFactory from './../../../app/services/storage.service'
import SessionsServiceFactory from './../../../app/services/sessions.service'
import DistributorsServiceFactory from './../../../app/services/distributors.service'

// Built by the core Angular team for mocking dependencies
import mocks from 'angular-mocks';

let module = angular.mock.module
let inject = angular.mock.inject


describe('WelcomeCtrl', function () {
  let $controller = undefined;
  let controller = undefined;
  let promise = undefined;
  let otherPromise = undefined;
  let versionData = undefined;
  let cookieMock = undefined;
  let $stateParams = undefined;
  let $state = undefined;
  let StorageService = undefined;
  let VersionsService = undefined;
  let SessionsService = undefined;
  let DistributorsService = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(module(function ($provide) {
    $provide.value('VersionsService', VersionsServiceFactory.create());
    $provide.value('StorageService', StorageServiceFactory.create());
    $provide.value('SessionsService', SessionsServiceFactory.create());
    $provide.value('DistributorsService', DistributorsServiceFactory.create());
  }));

  beforeEach(inject(function (_$controller_, _VersionsService_, _$state_, _StorageService_, _SessionsService_, _DistributorsService_) {
    $controller = _$controller_;
    $stateParams = {};
    $state = _$state_;
    VersionsService = _VersionsService_
    SessionsService = _SessionsService_
    StorageService = _StorageService_
    DistributorsService = _DistributorsService_

    controller = $controller('WelcomeCtrl', {
      VersionsService: _VersionsService_,
      StorageService: _StorageService_,
      SessionsService: _SessionsService_,
      $stateParams,
      $state,
      DistributorsService: _DistributorsService_
    });
  }));

  describe('initialization', () => {
    it('version_data should be an empty array', () => expect(angular.isArray(controller.version_data)).toBeTruthy())
  })


  return describe('.initialize', function () {
    versionData = [
      {
        web_version_name: 'snapshot',
        web_module_name: 'default',
        current_instance_id: '7bedeb21a1a3191ca8c5cd3dea9c99c0abee',
        default_version: 'snapshot',
        hostname: '127.0.0.1:8080'
      }
    ];

    beforeEach(function () {
      promise = new skykitProvisioning.q.Mock();
      otherPromise = new skykitProvisioning.q.Mock();
      spyOn($state, 'go');
      StorageService.removeAll();
      spyOn(VersionsService, 'getVersions').and.returnValue(promise);
      return spyOn(DistributorsService, 'fetchAllByUser').and.returnValue(otherPromise);
    });

    it('call VersionsService.getVersions to retrieve module version with auth', function () {
      StorageService.set("userEmail", "some.user@demo.agosto.com");
      controller.initialize();
      otherPromise.resolve(versionData);
      return expect(VersionsService.getVersions).toHaveBeenCalled();
    });

    it("the 'then' handler caches the retrieved version data on the controller with auth", function () {
      StorageService.set("userEmail", "some.user@demo.agosto.com");
      controller.initialize();
      otherPromise.resolve(versionData);
      promise.resolve(versionData);
      return expect(controller.version_data).toBe(versionData);
    });

    it('call VersionsService.getVersions to retrieve module version without auth', function () {
      controller.initialize();
      return expect($state.go).toHaveBeenCalledWith('sign_in');
    });


    return it("goes to sign in view when hit", function () {
      controller.proceedToSignIn();
      return expect($state.go).toHaveBeenCalledWith('sign_in');
    });
  });
});
