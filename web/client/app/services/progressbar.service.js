export default class ProgressBarService {
  /*@ngInject*/
  constructor(ngProgressFactory) {
    this.ngProgressFactory = ngProgressFactory
    this.progressBar = this.ngProgressFactory.createInstance();
  }

  start() {
    this.progressBar.setColor('#00FCFF');
    this.progressBar.setHeight('4px');
    return this.progressBar.start();
  }

  complete() {
    return this.progressBar.complete();
  }

  static create(ngProgressFactory) {
    return new ProgressBarService(ngProgressFactory)
  }
}
