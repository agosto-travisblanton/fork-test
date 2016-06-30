'use strict';

var gulp = require('gulp');
var order = require("gulp-order");
var dedupe = require("gulp-dedupe");

var $ = require('gulp-load-plugins')();

var wiredep = require('wiredep').stream;

module.exports = function (options) {
    gulp.task('inject', ['scripts', 'styles'], function () {
        var injectStyles = gulp.src([
            options.tmp + '/serve/app/**/*.css',
            '!' + options.tmp + '/serve/app/vendor.css'
        ], {read: false});

        var injectScripts = gulp.src([
            '{' + options.src + ',' + options.tmp + '/serve}/app/**/*.js',
            '!' + options.src + '/app/**/*.spec.js',
            '!' + options.src + '/app/**/*.mock.js'
            ])
            .pipe($.babel({
                presets: ['es2015']
            }))
            .pipe(order([
                "src/app/index.js",
            ]))
            .pipe(dedupe())

        var injectOptions = {
            ignorePath: [options.src, options.tmp + '/serve'],
            addRootSlash: false
        };

        return gulp.src(options.src + '/*.html')
            .pipe($.inject(injectStyles, injectOptions))
            .pipe(wiredep(options.wiredep))
            .pipe($.inject(injectScripts, injectOptions))
            .pipe(gulp.dest(options.tmp + '/serve'));

    });
};