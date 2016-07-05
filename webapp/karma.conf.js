'use strict';


var _ = require('lodash');
var wiredep = require('wiredep');


module.exports = function (config) {
    
    function listFiles() {
        var wiredepOptions = _.extend({}, {
            directory: 'bower_components',
            exclude: [/bootstrap-sass-official\/.*\.js/, /bootstrap\.css/]
        }, {
            dependencies: true,
            devDependencies: true
        });

        return wiredep(wiredepOptions).js
            .concat([
                'src/app/index.js',
                'src/app/**/*.js',
                'specs/**/*.js'
            ]);
    }

    var configuration = {
        // base path, that will be used to resolve files and exclude
        basePath: '.',

        //  # list of files / patterns to load in the browser
        files: listFiles(),

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
            'karma-babel-preprocessor',
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
            'src/**/*.js': ['babel', 'coverage'],
            'specs/**/*.js': ['babel'],
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
    
    config.set(configuration);
};
