import moment from 'moment'
export default class DateManipulationService {
  /*@ngInject*/

  constructor() {
  }

  convertToMomentIfNotAlready(date) {
    if (!moment.isMoment(date)) {
      return moment(new Date(date))
    } else {
      return date
    }
  }

  createFormattedStartAndEndDateFromToday(daysBack) {
    let startTime = moment().format('YYYY-MM-DD')
    let startTimeMidNight = moment(startTime, 'YYYY-MM-DD').format('YYYY-MM-DD hh:mm A')
    let startTimeEndOfDay = moment(startTimeMidNight, 'YYYY-MM-DD hh:mm A').add(1, 'day').subtract(60, 'seconds').format('YYYY-MM-DD hh:mm A')

    let endTime = moment().subtract(30, 'days').format('YYYY-MM-DD')
    let endTimeMidNight = moment(endTime, 'YYYY-MM-DD').format('YYYY-MM-DD hh:mm A')

    return [endTimeMidNight, startTimeEndOfDay]
  }

  generateLocalFromUTC(UTCTime) {
    let localTime = moment.utc(UTCTime).toDate();
    return moment(localTime).format('YYYY-MM-DD hh:mm:ss A');
  };

  static create(Restangular) {
    return new DateManipulationService()
  }
}





