angular.module('skykitProvisioning').factory('ProgressBarService', ngProgressFactory =>
    new class ProgressBarService {
        constructor() {
            this.progressBar = ngProgressFactory.createInstance();
        }

        start() {
            this.progressBar.setColor('#00FCFF');
            this.progressBar.setHeight('4px');
            return this.progressBar.start();
        }

        complete() {
            return this.progressBar.complete();
        }
    }()
);



