/*
 * When testing with Webpack and ES6, we have to do some
 * preliminary setup. Because we are writing our tests also in ES6,
 * we must transpile those as well, which is handled inside
 * `karma.conf.js` via the `karma-webpack` plugin. This is the entry
 * file for the Webpack tests. Similarly to how Webpack creates a
 * `bundle.js` file for the compressed app source files, when we
 * run our tests, Webpack, likewise, compiles and bundles those tests here.
 */
//
import install from 'jasmine-es6';
install();
import './client/app/app.js'
import 'angular-mocks';

angular.element(document).ready(function () {
  angular.bootstrap(document, ["skykitProvisioning"])
  console.log("##$#H$#$H#$HH#$#$$##$#$")

// // Built by the core Angular team for mocking dependencies

  let module = angular.mock.module
  let inject = angular.mock.inject


// We use the context method on `require` which Webpack created
// in order to signify which files we actually want to require or import.
// Below, `context` will be a/an function/object with file names as keys.
// Using that regex, we scan within `client/app` and target
// all files ending with `.spec.js` and trace its path.
// By passing in true, we permit this process to occur recursively.
  let context = require.context('./client/specs', true, /\.spec\.js/);

// Get all files, for each file, call the context function
// that will require the file and load it here. Context will
// loop and require those spec files here.
  context.keys().forEach(context);


})

