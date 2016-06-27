describe('ToastsService', function() {
  beforeEach(module('skykitProvisioning'));

  let ToastsService = undefined;
  let toastr = undefined;

  beforeEach(inject(function(_ToastsService_, _toastr_) {
    ToastsService = _ToastsService_;
    return toastr = _toastr_;
  }));

  describe('.showSuccessToast', function() {
    let expectedMessage = 'expected message!';
    let expectedTitle = 'Success!';

    beforeEach(() => spyOn(toastr, 'success'));

    it('defers to toastr.success', function() {
      ToastsService.showSuccessToast(expectedMessage);
      return expect(toastr.success).toHaveBeenCalledWith(expectedMessage, expectedTitle);
    });

    return it('defers to toastr.success with overridden title', function() {
      expectedTitle = 'Hey!';
      ToastsService.showSuccessToast(expectedMessage, expectedTitle);
      return expect(toastr.success).toHaveBeenCalledWith(expectedMessage, expectedTitle);
    });
  });

  describe('.showErrorToast', function() {
    let expectedMessage = 'expected message!';
    let expectedTitle = 'Error!';

    beforeEach(() => spyOn(toastr, 'error'));

    it('defers to toastr.error', function() {
      ToastsService.showErrorToast(expectedMessage);
      return expect(toastr.error).toHaveBeenCalledWith(expectedMessage, expectedTitle);
    });

    return it('defers to toastr.error with overridden title', function() {
      expectedTitle = 'Hey!';
      ToastsService.showErrorToast(expectedMessage, expectedTitle);
      return expect(toastr.error).toHaveBeenCalledWith(expectedMessage, expectedTitle);
    });
  });

  return describe('.showInfoToast', function() {
    let expectedMessage = 'expected message!';
    let expectedTitle = 'Information';

    beforeEach(() => spyOn(toastr, 'info'));

    it('defers to toastr.info', function() {
      ToastsService.showInfoToast(expectedMessage);
      return expect(toastr.info).toHaveBeenCalledWith(expectedMessage, expectedTitle);
    });

    return it('defers to toastr.info with overridden title', function() {
      expectedTitle = 'Hey!';
      ToastsService.showInfoToast(expectedMessage, expectedTitle);
      return expect(toastr.info).toHaveBeenCalledWith(expectedMessage, expectedTitle);
    });
  });
});
