'use strict';

var gulp = require('gulp');
var browserSync = require('browser-sync');

var $ = require('gulp-load-plugins')();

module.exports = function (options) {
    gulp.task('scripts', function () {
        return gulp.src(options.src + '/app/**/*.js')
            .pipe($.sourcemaps.init())
            .pipe($.babel({
                presets: ['es2015']
            }))
            .pipe($.sourcemaps.write())
            .pipe(gulp.dest(options.tmp + '/serve/app'))
            .pipe(browserSync.reload({stream: true}))
            .pipe($.size());
    });
};