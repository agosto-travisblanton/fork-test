'use strict';

module.exports = function (config) {

  var configuration = {
    // base path, that will be used to resolve files and exclude
    basePath: '.',

    //  # list of files / patterns to load in the browser
    files: [
      'bower_components/jquery/dist/jquery.js',
      'bower_components/lodash/lodash.js',
      'bower_components/bootstrap-sass-official/assets/javascripts/bootstrap.js',
      'bower_components/sweetalert/dist/sweetalert.min.js',
      'bower_components/angular/angular.js',
      'bower_components/angular-mocks/angular-mocks.js',
      'bower_components/angular-animate/angular-animate.js',
      'bower_components/angular-cookies/angular-cookies.js',
      'bower_components/angular-sanitize/angular-sanitize.js',
      'bower_components/angular-ui-router/release/angular-ui-router.js',
      'bower_components/angular-h-sweetalert/dist/ngSweetAlert.js',
      'bower_components/angular-toastr/dist/angular-toastr.js',
      'bower_components/restangular/dist/restangular.js',
      'bower_components/angular-bootstrap/ui-bootstrap.js',
      'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
      'bower_components/angular-breadcrumb/dist/angular-breadcrumb.js',
      'bower_components/angular-directive.g-signin/google-plus-signin.js',
      'bower_components/ngprogress/build/ngprogress.js',
      'bower_components/angular-bootstrap-datetimepicker-directive/angular-bootstrap-datetimepicker-directive.min.js',
      'bower_components/moment/min/moment.min.js',
      'bower_components/angular-material/angular-material.js', 
      'bower_components/angular-cache/dist/angular-cache.js',
      'bower_components/angular-aria/angular-aria.js',
      'bower_components/ngclipboard/src/ngclipboard.js',
      'src/app/index.coffee',
      'src/app/**/*.coffee',
      'specs/**/*.coffee'
    ],

    //  # list of files / patterns to exclude
    exclude: [],

    autoWatch: false,

    frameworks: ['jasmine'],

    ngHtml2JsPreprocessor: {
      stripPrefix: 'src/',
      moduleName: 'gulpAngular'
    },

    reporters: ['progress', 'coverage'],

    browsers: ['PhantomJS'],

    plugins: [
      'karma-phantomjs-launcher',
      'karma-chrome-launcher',
      'karma-jasmine',
      'karma-coverage',
      'karma-coffee-preprocessor',
      'karma-ng-html2js-preprocessor'
    ],

    port: 9090,

    //  Level of logging
    //  Possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
    logLevel: config.LOG_DEBUG,

    //  # Continuous Integration mode
    //  # if true, it capture browsers, run tests and exit
    singleRun: false,

    colors: true,

    preprocessors: {
      'src/**/*.coffee': ['coffee', 'coverage'],
      'specs/**/*.coffee': ['coffee'],
      'src/**/*.html': ['ng-html2js']
    },

    coverageReporter: {
      instrumenterOptions: {
        istanbul: {noCompact: true}
      },
      type: 'html',
      dir: 'coverage/'
    }
  };

  // This block is needed to execute Chrome on Travis
  // If you ever plan to use Chrome and Travis, you can keep it
  // If not, you can safely remove it
  // https://github.com/karma-runner/karma/issues/1144#issuecomment-53633076
  //if(configuration.browsers[0] === 'Chrome' && process.env.TRAVIS) {
  //  configuration.customLaunchers = {
  //    'chrome-travis-ci': {
  //      base: 'Chrome',
  //      flags: ['--no-sandbox']
  //    }
  //  };
  //  configuration.browsers = ['chrome-travis-ci'];
  //}

  config.set(configuration);
};
