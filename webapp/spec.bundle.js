/*
 * When testing with Webpack and ES6, we have to do some
 * preliminary setup. Because we are writing our tests also in ES6,
 * we must transpile those as well, which is handled inside
 * `karma.conf.js` via the `karma-webpack` plugin. This is the entry
 * file for the Webpack tests. Similarly to how Webpack creates a
 * `bundle.js` file for the compressed app source files, when we
 * run our tests, Webpack, likewise, compiles and bundles those tests here.
 */

import './src/app/index.js'

// Built by the core Angular team for mocking dependencies
import 'angular-mocks';


let module = angular.mock.module
let inject = angular.mock.inject

if (!window.skykitProvisioning) {
  window.skykitProvisioning = {};
}
if (!window.skykitProvisioning.q) {
  window.skykitProvisioning.q = {};
}

window.skykitProvisioning.q.Mock = class Mock {

  then(resolveFunc, rejectFunc) {
    this.resolveFunc = resolveFunc;
    if (rejectFunc) {
      this.canUseNormalCatch = true;
    }
    this.rejectFunc = rejectFunc;
    return;
  }

  catch(args) {
    if (this.canUseNormalCatch) {
      return this.rejectFunc(args);
    } else{
      return args
    }
  }

  resolve(args) {
    return this.resolveFunc(args);
  }

  reject(args) {
    return this.rejectFunc(args);
  }
};


// We use the context method on `require` which Webpack created
// in order to signify which files we actually want to require or import.
// Below, `context` will be a/an function/object with file names as keys.
// Using that regex, we scan within `client/app` and target
// all files ending with `.spec.js` and trace its path.
// By passing in true, we permit this process to occur recursively.
let context = require.context('./src/specs', true, /\.js/);

// Get all files, for each file, call the context function
// that will require the file and load it here. Context will
// loop and require those spec files here.
context.keys().forEach(context);


