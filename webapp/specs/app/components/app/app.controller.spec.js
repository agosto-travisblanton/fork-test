describe('AppController', function() {
  beforeEach(module('skykitProvisioning'));

  let $controller = undefined;
  let controller = undefined;
  let $window = undefined;
  let $mdSidenav = undefined;
  let $state = undefined;

  let sideNavFunction = {
    toggle() {},
    close() {},
    isOpen() { return true; }
  };

  beforeEach(module($provide =>
    $provide.decorator('$mdSidenav', function($delegate) {
      let sideNavSpy = jasmine.createSpy($delegate).and.returnValue(sideNavFunction);
      return sideNavSpy;
    })
  ));


  beforeEach(inject(function(_$controller_, _$state_, _$mdSidenav_, _$window_) {
    $controller = _$controller_;
    $state = _$state_;
    $mdSidenav = _$mdSidenav_;
    return $window = _$window_;
  }));

  describe('.initialize', function() {
    beforeEach(function() {
      controller = $controller('AppController');
      spyOn(controller, 'getIdentity');
      return controller.initialize();
    });

    it('calls getIdentity', () => expect(controller.getIdentity).toHaveBeenCalled());

    return it('determines isCurrentURLDistributorSelector', function() {
      let a = controller.isCurrentURLDistributorSelector();
      return expect(a).toBe(false);
    });
  });
  

  describe('.toggleSidenav', function() {
    beforeEach(function() {
      controller = $controller('AppController');
      spyOn(sideNavFunction, 'toggle');
      return controller.toggleSidenav();
    });

    it('invokes $mdSidenav with direction left', () => expect($mdSidenav).toHaveBeenCalledWith('left'));

    return it('invokes the toggle function on result of $mdSidenav', () => expect(sideNavFunction.toggle).toHaveBeenCalled());
  });

  return describe('.goTo', function() {
    let stateName = 'devices';
    let id = 5;
    let idParam = ({id});

    beforeEach(function() {
      spyOn($state, 'go');
      spyOn(sideNavFunction, 'close');
      return controller = $controller('AppController');
    });

    it('navigates to route with stateName and id', function() {
      controller.goTo(stateName, id);
      return expect($state.go).toHaveBeenCalledWith(stateName, idParam);
    });

    it('invokes $mdSidenav.close when $mdSidenav.isOpen is true', function() {
      controller.goTo(stateName, id);
      return expect(sideNavFunction.close).toHaveBeenCalled();
    });

    return it('will not invoke $mdSidenav.close when $mdSidenav.isOpen is false', function() {
      spyOn(sideNavFunction, 'isOpen').and.returnValue(false);
      controller.goTo(stateName, id);
      return expect(sideNavFunction.close).not.toHaveBeenCalled();
    });
  });
});
