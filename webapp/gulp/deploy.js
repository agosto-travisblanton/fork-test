'use strict';

var gulp = require('gulp');
var inject = require('gulp-inject');
var fs = require('fs')

module.exports = function (options) {


  gulp.task('moveFiles', ['build'], function () {
    return gulp.src([options.dist + '/**/*'])
      .pipe(gulp.dest(options.dist + '/../../static'));
  });


  gulp.task('deploy', ['moveFiles'], function () {
    fs.readFile('../static/index.html', 'utf8', function (err, data) {
      if (err) {
        return console.log(err);
      }
      var result = data.replace('<link rel="stylesheet" href="styles/vendor-dd06ce71.css"><link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', '<link rel="stylesheet" href="styles/vendor-dd06ce71.css"><link rel="stylesheet" href="styles/app.css"><link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">')

      fs.writeFile('../static/index.html', result, 'utf8', function (err) {
        if (err) return console.log(err);
      });
    });
  });


};
