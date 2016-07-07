describe('DateManipulationService', function () {
  let DateManipulationService = undefined;
  let promise = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_DateManipulationService_) {
    DateManipulationService = _DateManipulationService_;
    return promise = new skykitProvisioning.q.Mock();
  }));

  describe('.convertToMomentIfNotAlready', function () {
    it('returns the same object if it is a moment', function () {
      let momentObject = moment()
      let convertedToMoment = DateManipulationService.convertToMomentIfNotAlready(momentObject)
      expect(convertedToMoment).toEqual(momentObject)
    })

    it('returns the object as moment if it is a moment', function () {
      let momentObject = new Date()
      let convertedToMoment = DateManipulationService.convertToMomentIfNotAlready(momentObject)
      expect(convertedToMoment).toEqual(moment(new Date(momentObject)))
    })

  })

  describe('.createFormattedStartAndEndDateFromToday', function () {
    it('returns two dates originating from today', function () {
      let bothDates = DateManipulationService.createFormattedStartAndEndDateFromToday(30)
      let duration = moment.duration(moment(bothDates[0], 'YYYY-MM-DD hh:mm A').diff(moment(bothDates[1], 'YYYY-MM-DD hh:mm A')));
      let days = duration.asDays();
      expect(days).toBe(-30.999305555555555)
    })
  })

  describe('.generateLocalFromUTC', function () {
    it('returns a local time from a UTC', function () {
      let UTCTime = new Date().getTime();
      let localTime = DateManipulationService.generateLocalFromUTC(UTCTime).toString()
      expect(localTime.indexOf("UTC") >= 0).toEqual(false)
    })
  })

});

