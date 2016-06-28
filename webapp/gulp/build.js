'use strict';

var gulp = require('gulp');
var wiredep = require('wiredep').stream;
var order = require("gulp-order");
var dedupe = require("gulp-dedupe");
var rimraf = require('rimraf');

var $ = require('gulp-load-plugins')({
    pattern: ['gulp-*', 'main-bower-files', 'del']
});

var sass = require('gulp-sass');
var gulpBowerFiles = require('gulp-bower-files');
var gulp = require('gulp');
var concat = require('gulp-concat');
var minCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var filever = require('gulp-version-filename');
var s3 = require("gulp-s3-ls");

/**
 * Aggregate the files.
 *
 * Note that these files are explicitly defined instead of fetching all files
 * from the dir because the concat order of CSS files matter, by definition.
 */
module.exports = function (options) {

    gulp.task('minCSS', [], function () {
        gulp.src('src/app/*.scss', gulpBowerFiles())
            .pipe($.filter('**/*.css'))
            .pipe(sass().on('error', sass.logError))
            .pipe(concat('vendor.css'))
            .pipe(minCss({
                keepSpecialComments: 1
            }))
            .pipe(gulp.dest(options.dist + '/'));
        ;
    });

    /**
     * Minify the JS files.
     *
     * We need to preserve comments to allow for versioning later
     */
    gulp.task('minJS', [], function () {
        var injectScripts = gulp.src([
            'src/app/**/*.js',
        ])
            .pipe(order([
                "**/index.js",
                '**/*.js'
            ]))
            .pipe(concat('common.js'))
            .pipe($.babel({
                presets: ['es2015']
            }))
            .pipe(gulp.dest(options.dist + '/'));


        var injectOptions = {
            ignorePath: [options.src, options.tmp + '/serve'],
            addRootSlash: false
        };

        var injectDeps = gulpBowerFiles()
            .pipe($.filter('**/*.js'))
            .pipe(concat('vendor.js'))
            .pipe(gulp.dest(options.dist + '/'));

        var sources = gulp.src([options.dist + '/vendor.js', options.dist + '/common.js'], {read: false});

        return gulp.src(options.src + '/*.html')
            .pipe($.inject(sources, injectOptions))
            .pipe(gulp.dest(options.dist + '/'));

    });

    gulp.task('partials', function () {
        return gulp.src([
            options.src + '/app/**/*.html',
            options.tmp + '/serve/app/**/*.html'
        ])
            .pipe($.minifyHtml({
                empty: true,
                spare: true,
                quotes: true
            }))
            .pipe($.angularTemplatecache('templateCacheHtml.js', {
                module: 'skykitProvisioning',
                root: 'app'
            }))
            .pipe(gulp.dest(options.tmp + '/partials/'));
    });


    // Only applies for fonts from bower dependencies
    // Custom fonts are handled by the "other" task
    gulp.task('fonts', function () {
        return gulp.src($.mainBowerFiles())
            .pipe($.filter('**/*.{eot,svg,ttf,woff,woff2}'))
            .pipe($.flatten())
            .pipe(gulp.dest(options.dist + '/fonts/'));
    });

    gulp.task('other', function () {
        return gulp.src([
            options.src + '/**/*',
            '!' + options.src + '/**/*.{html,css,scss,coffee}'
        ])
            .pipe(gulp.dest(options.dist + '/'));
    });

    gulp.task('clean', function (done) {
        $.del([options.dist + '/', options.tmp + '/'], done);
    });

    gulp.task('build', ['minJS', 'minCSS', 'fonts', 'other']);
};
