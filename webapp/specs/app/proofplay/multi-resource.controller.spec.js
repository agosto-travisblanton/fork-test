describe('ProofOfPlayMultiResourceCtrl', function () {
    let $controller = undefined;
    let controller = undefined;
    let ProofPlayService = undefined;
    let $stateParams = undefined;
    let $state = undefined;
    let ToastsService = undefined;
    let promise = undefined;
    let selected_tenant = undefined;

    beforeEach(module('skykitProvisioning'));

    beforeEach(inject(function (_$controller_, _ProofPlayService_, _ToastsService_, _$state_) {
        $controller = _$controller_;
        ProofPlayService = _ProofPlayService_;
        ToastsService = _ToastsService_;
        $stateParams = {};
        $state = _$state_;
        return controller = $controller('ProofOfPlayMultiResourceCtrl', {
            ProofPlayService,
            ToastsService,
            $stateParams,
            $state
        });
    }));

    describe('initialization', function () {
        it('radioButtonChoices should equal', function () {
            let radioButtonChoices = {
                group1: 'By Device',
                group2: 'By Date',
                selection: null
            };
            return expect(angular.equals(radioButtonChoices, controller.radioButtonChoices)).toBeTruthy();
        });

        it('dateTimeSelection should equal', function () {
            let dateTimeSelection = {
                start: null,
                end: null
            };
            return expect(angular.equals(dateTimeSelection, controller.dateTimeSelection)).toBeTruthy();
        });


        it('dateTimeSelection should equal', function () {
            let formValidity = {
                start_date: false,
                end_date: false,
                resources: false,
            };
            return expect(angular.equals(formValidity, controller.formValidity)).toBeTruthy();
        });

        return it('config objects should equal', function () {
            expect(controller.no_cache).toBeTruthy();
            expect(controller.loading).toBeTruthy();
            expect(controller.disabled).toBeTruthy();
            return expect(angular.isArray(controller.selected_resources)).toBeTruthy();
        });
    });


    describe('.initialize', function () {
        let resourcesData = {
            data: {
                resources: [{"resource_name": "one resource"}]
            }
        };

        beforeEach(function () {
            promise = new skykitProvisioning.q.Mock();
            let querySearch = function () {
            };
            spyOn($state, 'go');
            spyOn(ProofPlayService, 'getAllResources').and.returnValue(promise);
            spyOn(ProofPlayService, 'querySearch').and.returnValue(querySearch);
            spyOn(ProofPlayService, 'downloadCSVForMultipleResourcesByDate').and.returnValue(true);
            return spyOn(ProofPlayService, 'downloadCSVForMultipleResourcesByDevice').and.returnValue(true);
        });


        it('call getAllResources to populate autocomplete with resources', function () {
            controller.initialize();
            return expect(ProofPlayService.getAllResources).toHaveBeenCalled();
        });


        it('call querySearch accesses service', function () {
            controller.initialize();
            controller.querySearch(resourcesData.data.resources, "one");
            return expect(ProofPlayService.querySearch).toHaveBeenCalled();
        });

        it("isRadioValid function sets formValidity type", function () {
            controller.isRadioValid("test");
            return expect(controller.formValidity.type).toBe("test");
        });

        it("the 'then' handler caches the retrieved resources data in the controller and loading to be done", function () {
            controller.initialize();
            promise.resolve(resourcesData);
            expect(controller.full_resource_map).toBe(resourcesData.data.resources);
            return expect(controller.loading).toBeFalsy();
        });


        it('isStartDateValid sets formValidity start_date', function () {
            let someDate = new Date();
            controller.isStartDateValid(someDate);
            return expect(controller.formValidity.start_date).toBe(true);
        });

        it('isEndDateValid sets formValidity end_date', function () {
            let someDate = new Date();
            controller.isEndDateValid(someDate);
            return expect(controller.formValidity.end_date).toBe(true);
        });


        it('isResourceValid returns validity', function () {
            controller.initialize();
            promise.resolve(resourcesData);

            controller.selected_resources = [resourcesData.data.resources[0]["resource_name"]];
            let resourceValidity = controller.isResourceValid(resourcesData.data.resources[0]["resource_name"]);
            expect(resourceValidity).toBeFalsy();
            controller.selected_resources = [];
            let newResourceValidity = controller.isResourceValid(resourcesData.data.resources[0]["resource_name"]);
            expect(newResourceValidity).toBeTruthy();
            newResourceValidity = controller.isResourceValid("something not in resources");
            return expect(newResourceValidity).toBeFalsy();
        });


        it('areResourcesValid sets formValidity resources value', function () {
            controller.selected_resources = ["at least one value here"];
            controller.areResourcesValid();
            return expect(controller.formValidity.resources).toBeTruthy();
        });

        it('disabled is false if formValidity keys are true', function () {
            controller.formValidity.start_date = true;
            controller.formValidity.end_date = true;
            controller.formValidity.resources = true;
            controller.formValidity.type = true;
            controller.isDisabled();
            return expect(controller.disabled).toBeFalsy();
        });


        it('adds to selected resource if resource is valid', function () {
            controller.initialize();
            promise.resolve(resourcesData);
            controller.addToSelectedResources(resourcesData.data.resources[0]["resource_name"]);
            expect(angular.equals(controller.resources, [])).toBeTruthy();
            return expect(angular.equals(controller.selected_resources, ['one resource'])).toBeTruthy();
        });


        it('removes from selected resource', function () {
            controller.initialize();
            promise.resolve(resourcesData);
            controller.addToSelectedResources(resourcesData.data.resources[0]);
            controller.removeFromSelectedResource(resourcesData.data.resources[0]);
            return expect(controller.selected_resources.length).toEqual(0);
        });


        return it('opens window when submit gets called', function () {
            controller.final = {
                start_date_unix: moment(new Date()).unix(),
                end_date_unix: moment(new Date()).unix(),
                resources: ["one resource"],
                type: "1"
            };
            controller.full_resource_map = resourcesData.data.resources;

            controller.submit();
            expect(ProofPlayService.downloadCSVForMultipleResourcesByDevice).toHaveBeenCalled();

            controller.final.type = "2";
            controller.submit();
            return expect(ProofPlayService.downloadCSVForMultipleResourcesByDate).toHaveBeenCalled();
        });
    });

    return describe('.tenant change related functions', function () {
        selected_tenant = "some_tenant";
        let resourcesData = {
            data: {
                resources: [{"resource_name": "one resource"}]
            }
        };

        beforeEach(function () {
            promise = new skykitProvisioning.q.Mock();
            spyOn(ProofPlayService, 'getAllResources').and.returnValue(promise);
            spyOn(ProofPlayService, 'getAllTenants').and.returnValue(promise);
            return spyOn($state, 'go');
        });


        it('initializeTenantSelection sets tenants', function () {
            controller.initialize_tenant_select();
            let to_resolve = {
                data: {
                    tenants: ["one", "two"]
                }
            };
            promise.resolve(to_resolve);
            return expect(controller.tenants).toEqual(["one", "two"]);
        });


        return it('submitTenants sets currentTenant and getsAllDisplays again', function () {
            controller.submitTenant(selected_tenant);
            return expect($state.go).toHaveBeenCalledWith('proofDetail', {tenant: selected_tenant});
        });
    });
});
