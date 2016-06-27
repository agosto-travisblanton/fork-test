angular.module('skykitProvisioning').factory('StorageService', () =>
  new class StorageService {

    constructor() {}

    set(key, value) {
      return Lockr.set(key, value);
    }

    get(key) {
      return Lockr.get(key);
    }
      
    rm(key) {
      return Lockr.rm(key);
    }

    removeAll() {
      return Lockr.flush();
    }
  }()
);

