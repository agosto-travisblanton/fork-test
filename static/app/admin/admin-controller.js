(function () {


    let app = angular.module('skykitProvisioning');

    app.controller("AdminCtrl", function (AdminService,
                                          SessionsService,
                                          ToastsService,
                                          $mdDialog,
                                          DistributorsService) {
        let vm = this;

        vm.getAllDistributors = function () {
            vm.loadingAllDistributors = true;
            let getAllDistributorsPromise = AdminService.getAllDistributors();
            return getAllDistributorsPromise.then(function (data) {
                vm.loadingAllDistributors = false;
                return vm.allDistributors = data;
            });
        };

        vm.addUserToDistributor = function (ev, userEmail, distributorAdmin, whichDistributor, form) {
            if (!distributorAdmin) {
                distributorAdmin = false;
            }
            let withOrWithout = distributorAdmin ? "with" : "without";

            // no option to select distributor is given when there is only one option
            if (!whichDistributor) {
                whichDistributor = vm.distributorsAsAdmin[0];
            }

            let confirm = $mdDialog.confirm(
                {
                    title: 'Are you sure?',
                    textContent: `${userEmail} will be added to ${whichDistributor}
        ${withOrWithout} administrator privileges`,
                    targetEvent: ev,
                    ok: 'Of course!',
                    cancel: 'Oops, nevermind.'
                }
            );

            return $mdDialog.show(confirm).then(function () {
                let addUserToDistributorPromise = AdminService.addUserToDistributor(userEmail, whichDistributor, distributorAdmin);
                addUserToDistributorPromise.then(function (data) {
                    ToastsService.showSuccessToast(data.message);
                    vm.user = {};
                    form.$setPristine();
                    form.$setUntouched();
                    return setTimeout((() => vm.getUsersOfDistributor()), 2000);
                });

                return addUserToDistributorPromise.catch(data => ToastsService.showErrorToast(data.data.message));
            });
        };

        vm.makeDistributor = function (ev, distributorName, adminEmail, form) {
            let confirm = $mdDialog.confirm(
                {
                    title: 'Are you sure?',
                    textContent: `If you proceed, ${distributorName} will be created.`,
                    targetEvent: ev,
                    ariaLabel: 'Lucky day',
                    ok: 'Yeah!',
                    cancel: 'Forget it.'
                }
            );
            return $mdDialog.show(confirm).then((function () {
                let makeDistributorPromise = AdminService.makeDistributor(distributorName, adminEmail);
                makeDistributorPromise.then(function (data) {
                    vm.distributor = {};
                    form.$setPristine();
                    form.$setUntouched();
                    ToastsService.showSuccessToast(data.message);
                    return setTimeout((() => vm.allDistributors = vm.getAllDistributors()), 2000);
                });

                return makeDistributorPromise.catch(data => ToastsService.showErrorToast(data.data.message));
            }));
        };

        vm.getUsersOfDistributor = function () {
            vm.loadingUsersOfDistributor = true;
            let currentDistributorKey = SessionsService.getCurrentDistributorKey();
            let usersofDistributorPromise = AdminService.getUsersOfDistributor(currentDistributorKey);
            return usersofDistributorPromise.then(function (data) {
                vm.loadingUsersOfDistributor = false;
                return vm.usersOfDistributor = data;
            });
        };

        vm.switchDistributor = function (distributor) {
            DistributorsService.switchDistributor(distributor);
            return ToastsService.showSuccessToast(`Distributor ${distributor.name} selected!`);
        };

        vm.initialize = function () {
            vm.getUsersOfDistributor();
            vm.getAllDistributors();
            vm.isAdmin = SessionsService.getIsAdmin();
            vm.distributorsAsAdmin = SessionsService.getDistributorsAsAdmin();
            vm.currentDistributorName = SessionsService.getCurrentDistributorName();

            if (vm.isAdmin) {
                return vm.getAllDistributors();
            }
        };

        return vm;
    });

})
();