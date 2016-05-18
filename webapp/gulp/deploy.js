'use strict';

var gulp = require('gulp');

module.exports = function (options) {
  gulp.task('deploy', ['build'], function () {
    return gulp.src([options.dist + '/**/*', '!' + options.dist + '/app/**/*'])
      .pipe(gulp.dest(options.dist + '/../../static'));
  });
};
