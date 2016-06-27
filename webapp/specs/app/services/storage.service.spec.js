describe('StorageService', function() {
  beforeEach(module('skykitProvisioning'));
  let StorageService = undefined;
  let key = undefined; 
  let value = undefined;

  beforeEach(inject(function(_StorageService_) {
    StorageService = _StorageService_;
    key = "jim";
    return value = "dwight";
  }));

  return describe('StorageService API', function() {
    it('sets then gets a value for a key', function() {
      StorageService.set(key, value);
      return expect(StorageService.get(key)).toEqual(value);
    });
      
    it('sets than does not get a value for key after removal of key', function() {
      StorageService.set(key, value);
      StorageService.rm(key);
      return expect(StorageService.get(key)).toEqual(undefined);
    });
  
    return it('sets than does not get a value for key after removeAll', function() {
      StorageService.set(key, value);
      let pam = "pam";
      StorageService.set(pam, "angela");
      StorageService.removeAll();
      expect(StorageService.get(key)).toEqual(undefined);
      return expect(StorageService.get(pam)).toEqual(undefined);
    });
  });
});
      