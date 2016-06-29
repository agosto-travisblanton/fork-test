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
var injectOptions;
var sources;
var appCSS;
var bowerCSS;
/**
 * Aggregate the files.
 *
 * Note that these files are explicitly defined instead of fetching all files
 * from the dir because the concat order of CSS files matter, by definition.
 */
module.exports = function (options) {


    gulp.task('minCSS', [], function () {
        appCSS = gulp.src('src/app/**/*.scss')
            .pipe(sass().on('error', sass.logError))
            .pipe(minCss())
            .pipe(concat('styles/app.css'))
            .pipe(gulp.dest(options.dist + '/'));


        var partialsInjectFile = gulp.src(options.tmp + '/partials/templateCacheHtml.js', {read: false});
        var partialsInjectOptions = {
            starttag: '<!-- inject:partials -->',
            ignorePath: options.tmp + '/partials',
            addRootSlash: false
        };

        var htmlFilter = $.filter('*.html');
        var jsFilter = $.filter('**/*.js');
        var cssFilter = $.filter('**/*.css');
        var assets;

        return gulp.src(options.tmp + '/serve/*.html')
            .pipe($.inject(partialsInjectFile, partialsInjectOptions))
            .pipe(assets = $.useref.assets())
            .pipe($.rev())
            .pipe(cssFilter)
            .pipe($.replace('../../bower_components/bootstrap-sass-official/assets/fonts/bootstrap/', '../fonts/'))
            .pipe($.csso())
            .pipe(assets.restore())
            .pipe($.useref())
            .pipe($.revReplace())
            .pipe(htmlFilter)
            .pipe($.minifyHtml({
                empty: true,
                spare: true,
                quotes: true,
                conditionals: true
            }))
            .pipe(htmlFilter.restore())
            .pipe(gulp.dest(options.dist + '/'))
            .pipe($.size({title: options.dist + '/', showFiles: true}));
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
            .pipe(concat('scripts/app.js'))
            .pipe($.babel({
                presets: ['es2015']
            }))
            .pipe(gulp.dest(options.dist + '/'));


        injectOptions = {
            ignorePath: [options.src, options.tmp + '/serve'],
            addRootSlash: false
        };

        var injectDeps = gulpBowerFiles()
            .pipe($.filter('**/*.js'))
            .pipe(concat('scripts/vendor.js'))
            .pipe(gulp.dest(options.dist + '/'));

        sources = gulp.src([options.dist + '/vendor.js', options.dist + '/common.js'], {read: false});


    });

    gulp.task('html', function () {
        return gulp.src(options.src + '/*.html')
            .pipe($.inject(sources, injectOptions))
            .pipe($.inject(appCSS, injectOptions))
            .pipe($.inject(bowerCSS, injectOptions))
            .pipe(gulp.dest(options.dist + '/'));
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
