import mocks from 'angular-mocks';
let module = angular.mock.module
let inject = angular.mock.inject

describe('ImageService', function () {
  let ImageService = undefined;
  let Restangular = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_ImageService_, _Restangular_) {
    ImageService = _ImageService_;
    Restangular = _Restangular_;
    return promise = new skykitProvisioning.q.Mock();
  }));


  describe('.getImages', () =>
    it('gets Images, returning a promise', function () {
      let tenant = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'};
      let imageRestangularService = {
        getList() {
        }
      };
      spyOn(Restangular, 'oneUrl').and.returnValue(imageRestangularService);
      spyOn(imageRestangularService, 'getList').and.returnValue(promise);
      let actual = ImageService.getImages(tenant.key);
      expect(Restangular.oneUrl).toHaveBeenCalledWith('image', `/api/v1/image/tenant/${tenant.key}`);
      expect(imageRestangularService.getList).toHaveBeenCalled();
      return expect(actual).toBe(promise);
    })
  );

  // Todo: Fix this test to test jQuery ajax call
  // describe('.saveImage', () =>
  //   it('saves Image, returning a promise', function () {
  //     let tenant = {key: 'dhYUYdfhdjfhlasddf7898a7sdfdas78d67', name: 'Foobar'};
  //     let imageRestangularService = {
  //       customPOST() {
  //       }
  //     };
  //     let svg_rep = "<xml>";
  //     let name = "some name";
  //     spyOn(Restangular, 'oneUrl').and.returnValue(imageRestangularService);
  //     spyOn(imageRestangularService, 'customPOST').and.returnValue(promise);
  //     let search = ImageService.saveImage(tenant.key, svg_rep, name);
  //     expect(Restangular.oneUrl).toHaveBeenCalledWith('image', `/api/v1/image/tenant/${tenant.key}`);
  //     expect(imageRestangularService.customPOST).toHaveBeenCalled();
  //     return expect(search).toBe(promise)
  //   })
  // );
});
