describe('AdminCtrl', function () {
  beforeEach(module('skykitProvisioning'));

  let $controller = undefined;
  let controller = undefined;
  let ToastsService = undefined;
  let $mdDialog = undefined;
  let AdminService = undefined;
  let DistributorsService = undefined;
  let SessionsService = undefined;
  let getAllDistributorsPromise = undefined;
  let angularForm = undefined;
  let getUsersOfDistributorPromise = undefined;
  let currentDistributorName = 'current';

  beforeEach(inject(function (_$controller_, _$mdDialog_, _ToastsService_, _DistributorsService_, _SessionsService_, _AdminService_) {
    $controller = _$controller_;
    SessionsService = _SessionsService_;
    ToastsService = _ToastsService_;
    AdminService = _AdminService_;
    DistributorsService = _DistributorsService_;
    return $mdDialog = _$mdDialog_;
  }));

  return describe('.initialize', function () {
    beforeEach(function () {
      controller = $controller('AdminCtrl', {
        SessionsService,
        ToastsService,
        DistributorsService,
        $mdDialog,
        AdminService
      });

      getAllDistributorsPromise = new skykitProvisioning.q.Mock();
      let mdDialogPromise = new skykitProvisioning.q.Mock();
      let addUserToDistributorPromise = new skykitProvisioning.q.Mock();
      let makeDistributorPromise = new skykitProvisioning.q.Mock();
      getUsersOfDistributorPromise = new skykitProvisioning.q.Mock();

      spyOn(ToastsService, 'showSuccessToast');
      spyOn(ToastsService, 'showErrorToast');
      spyOn(DistributorsService, 'switchDistributor');

      spyOn(SessionsService, 'getIsAdmin').and.returnValue(true);
      spyOn(SessionsService, 'getDistributorsAsAdmin').and.returnValue([]);
      spyOn(SessionsService, 'getCurrentDistributorName').and.returnValue(currentDistributorName);
      spyOn(SessionsService, 'getCurrentDistributorKey').and.returnValue([]);

      spyOn(AdminService, 'getUsersOfDistributor').and.returnValue(getUsersOfDistributorPromise);
      spyOn(AdminService, 'addUserToDistributor').and.returnValue(addUserToDistributorPromise);
      spyOn(AdminService, 'makeDistributor').and.returnValue(makeDistributorPromise);
      spyOn(AdminService, 'getAllDistributors').and.returnValue(getAllDistributorsPromise);
      spyOn($mdDialog, 'show').and.returnValue(mdDialogPromise);

      spyOn($mdDialog, 'confirm').and.callFake(() => 'ok');

      return angularForm = {
        $setPristine() {
        },

        $setUntouched() {
        }
      };
    });

    it('.getsAllDistributors', function () {
      controller.getAllDistributors();
      expect(controller.loadingAllDistributors).toBe(true);
      let distributors = ["one", "two"];
      getAllDistributorsPromise.resolve(distributors);
      expect(controller.loadingAllDistributors).toBe(false);
      return expect(controller.allDistributors).toEqual(distributors);
    });

    it('.addUserToDistributor', function () {
      let jquery_event = {};
      let userEmail = {email: "test@gmail.com"};
      let distributorAdmin = false;
      let whichDistributor = "someDistributor";
      let withOrWithout = distributorAdmin ? "with" : "without";
      controller.addUserToDistributor(jquery_event, userEmail, distributorAdmin, whichDistributor, angularForm);
      let confirm = $mdDialog.confirm(
        {
          title: 'Are you sure?',
          textContent: `${userEmail} will be added to ${whichDistributor}
      ${withOrWithout} administrator priviledges`,
          targetEvent: jquery_event,
          ok: 'Of course!',
          cancel: 'Oops, nevermind.'
        }
      );
      expect($mdDialog.show).toHaveBeenCalledWith(confirm);
      return expect(AdminService.addUserToDistributor).toHaveBeenCalled;
    });


    it('.makeDistributor', function () {
      let jquery_event = {};
      let adminEmail = {email: "test@gmail.com"};
      let distributorName = "someDistributor";
      controller.makeDistributor(jquery_event, distributorName, adminEmail, angularForm);
      let confirm = $mdDialog.confirm(
        {
          title: 'Are you sure?',
          textContent: `If you proceed, ${distributorName} will be created.`,
          targetEvent: jquery_event,
          ariaLabel: 'Lucky day',
          ok: 'Yeah!',
          cancel: 'Forget it.'
        }
      );
      expect($mdDialog.show).toHaveBeenCalledWith(confirm);
      return expect(AdminService.makeDistributor).toHaveBeenCalled;
    });

    it('.getUsersOfDistributor', function () {
      controller.getUsersOfDistributor();
      return expect(controller.loadingUsersOfDistributor).toBe(true);
    });

    it('.switchDistributor', function () {
      let distributor = {name: "test"};
      controller.switchDistributor(distributor);
      return expect(ToastsService.showSuccessToast).toHaveBeenCalledWith(
        `Distributor ${distributor.name} selected!`);
    });

    return it('.initialize', function () {
      controller.initialize();
      expect(controller.currentDistributorName).toEqual(currentDistributorName);
      expect(controller.isAdmin).toEqual(true);
      return expect(controller.distributorsAsAdmin).toEqual([]);
    });
  });
});
