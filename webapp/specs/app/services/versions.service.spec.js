describe('VersionsService', function () {
    let VersionsService = undefined;
    let Restangular = undefined;
    let promise = undefined;

    beforeEach(module('skykitProvisioning'));

    beforeEach(inject(function (_VersionsService_, _Restangular_) {
        VersionsService = _VersionsService_;
        Restangular = _Restangular_;
        return promise = new skykitProvisioning.q.Mock();
    }));

    return describe('.getVersions', function () {
        let versionsRestangularService = undefined;
        let result = undefined;

        beforeEach(function () {
            versionsRestangularService = {
                get() {
                }
            };
            spyOn(Restangular, 'oneUrl').and.returnValue(versionsRestangularService);
            spyOn(versionsRestangularService, 'get').and.returnValue(promise);
            return result = VersionsService.getVersions();
        });

        it('obtains Restangular service for version', () => expect(Restangular.oneUrl).toHaveBeenCalledWith('versions'));

        it('obtains the versions from the Restangular service', () => expect(versionsRestangularService.get).toHaveBeenCalled());

        return it('returns a promise', () => expect(result).toBe(promise));
    });
});

