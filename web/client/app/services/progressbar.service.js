export default class ProgressBarService {
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

}

ProgressBarService.$inject = [
  "ngProgressFactory",
]
