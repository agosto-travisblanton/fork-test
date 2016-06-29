describe('TimezonesService', function () {
    let TimezonesService = undefined;
    let Restangular = undefined;
    let promise = undefined;

    beforeEach(module('skykitProvisioning'));

    beforeEach(inject(function (_TimezonesService_, _Restangular_) {
        TimezonesService = _TimezonesService_;
        Restangular = _Restangular_;
        return promise = new skykitProvisioning.q.Mock();
    }));

    return describe('.getTimezones', () =>
        it('retrieve list of timezones, returning a promise', function () {
            let timezonesRestangularService = {
                get() {
                }
            };
            spyOn(Restangular, 'oneUrl').and.returnValue(timezonesRestangularService);
            spyOn(timezonesRestangularService, 'get').and.returnValue(promise);
            let actual = TimezonesService.getUsTimezones(promise);
            expect(Restangular.oneUrl).toHaveBeenCalledWith('timezones', 'api/v1/timezones/us');
            expect(timezonesRestangularService.get).toHaveBeenCalled();
            return expect(actual).toBe(promise);
        })
    );
});
