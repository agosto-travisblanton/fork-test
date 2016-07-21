import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

import StorageServiceClass from './../../../app/services/storage.service'//

describe('StorageService', function () {
  let StorageService = undefined;
  let key = undefined;
  let value = undefined;
  
  beforeEach(module('skykitProvisioning'));
  
  beforeEach((function () {
    StorageService = new StorageServiceClass();
    key = "jim";
    value = "dwight";
  }));

  return describe('StorageService API', function () {
    it('sets then gets a value for a key', function () {
      StorageService.set(key, value);
      return expect(StorageService.get(key)).toEqual(value);
    });

    it('sets than does not get a value for key after removal of key', function () {
      StorageService.set(key, value);
      StorageService.rm(key);
      return expect(StorageService.get(key)).toEqual(null);
    });

    return it('sets than does not get a value for key after removeAll', function () {
      StorageService.set(key, value);
      let pam = "pam";
      StorageService.set(pam, "angela");
      StorageService.removeAll();
      expect(StorageService.get(key)).toEqual(null);
      return expect(StorageService.get(pam)).toEqual(null);
    });
  });
});
