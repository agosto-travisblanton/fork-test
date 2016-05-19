'use strict';

var gulp = require('gulp');
var karma = require('karma').server;


module.exports = function (options) {

  gulp.task('test', function (done) {
    karma.start({configFile: __dirname + '/../karma.conf.js', singleRun: true}, done);
  });
};

