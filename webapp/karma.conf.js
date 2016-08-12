var webpack = require("webpack")
var path = require('path')
var fs = require('fs');

var root = 'src';
var modifiedSpecBundleName = 'spec.bundle.specific.js'

var determineIfValidDirectoryOrFile = function (path) {
  var stats = fs.lstatSync('./src/specs/' + path);
  return (stats.isDirectory() || stats.isFile())
}

var determineFileToUse = function (config) {
  if (config.path) {
    return modifiedSpecBundleName
  } else {
    return 'spec.bundle.js'
  }
}

var writeNewSpecBundleWithPath = function (path) {
  var data = fs.readFileSync('./spec.bundle.js', {encoding: 'utf8'});
  if (!(path.includes(".js"))) {
    var newData = data.replace("./src/specs", "./src/specs/" + path);
    fs.writeFileSync(modifiedSpecBundleName, newData);
  } else {
    var newData = data.replace("require.context('./src/specs', true, /\\.js/", "require('./src/specs/" + path + "'");
    newData = newData.replace('context.keys().forEach(context);', "")
    fs.writeFileSync(modifiedSpecBundleName, newData);
  }
}


module.exports = function (config) {
  if (config.path) {
    if (determineIfValidDirectoryOrFile(config.path)) {
      writeNewSpecBundleWithPath(config.path)
    } else {
      console.log("THIS IS NOT A VALID PATH")
      process.exit(1)
    }
  }

  var fileToUse = determineFileToUse(config)
  var preproccesors = {}
  preproccesors[fileToUse] = ['webpack', 'sourcemap']

  config.set({
    // base path used to resolve all patterns
    basePath: '',

    browserNoActivityTimeout: 60000, // 60 seconds

    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],

    // list of files/patterns to load in the browser
    files: [{pattern: fileToUse, watched: false}],

    // files to exclude
    exclude: [],

    plugins: [
      require("karma-phantomjs-launcher"),
      require("karma-chai"),
      require('karma-jasmine'),
      require("karma-chrome-launcher"),
      require("karma-mocha"),
      require("karma-mocha-reporter"),
      require("karma-sourcemap-loader"),
      require("karma-webpack")
    ],

    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: preproccesors,

    webpack: {
      devtool: 'inline-source-map',
      module: {
        loaders: [
          {test: /\.js$/, exclude: [/app\/lib/, /node_modules/, /bower_components/], loader: 'ng-annotate!babel'},
          {test: /\.html$/, loader: 'raw'},
          {test: /\.scss$/, loaders: ['style', 'css', 'sass']},
          {test: /\.styl$/, loader: 'style!css!stylus'},
          {test: /\.css$/, loader: 'style!css'},
          {test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/font-woff'},
          {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
          {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
          {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'}
        ]
      },
      plugins: [
        new webpack.ProvidePlugin({
          $: "jquery",
          jQuery: "jquery"
        })

      ]
    },

    logLevel: config.LOG_INFO,

    webpackServer: {
      noInfo: true // prevent console spamming when running in Karma!
    },

    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],

    // web server port
    port: 9876,

    // enable colors in the output
    colors: true,

    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,

    // toggle whether to watch files and rerun tests upon incurring changes
    autoWatch: false,

    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['PhantomJS'],

    // if true, Karma runs tests once and exits
    singleRun: true
  });
};
