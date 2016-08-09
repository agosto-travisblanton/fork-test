import angular from 'angular';
import uiRouter from 'angular-ui-router';
import moment from 'moment';
import 'angular-tooltips';
import './components/angular-material-fileinput/lf-ng-md-file-input.css'
import './components/angular-material-fileinput/lf-ng-md-file-input'
import 'angular-tooltips/dist/angular-tooltips.css'
import 'angular-toastr/dist/angular-toastr.css'
import 'angular-toastr';
import "font-awesome/css/font-awesome.css";
import 'normalize.css';
import "bootstrap-webpack";
import './components/ngProgress/ngProgress';
import './components/ngProgress/ngProgress.css';
import './components/angularBreadcrumb/angularBreadcrumb';
import './components/angular-material-datetimepicker/js/angular-material-datetimepicker'
import './components/angular-material-datetimepicker/css/material-datetimepicker.css'
import './components/angular-directive.g-signin/google-plus-signin'
import 'restangular';
import 'angular-material'
import 'sweetalert';
import 'angular-h-sweetalert';
import 'sweetalert/dist/sweetalert.css';
import 'angular-toastr';
import 'angular-cookies';
import 'angular-sanitize';
import 'angular-ui-bootstrap';
import 'ngclipboard';
import 'jquery';
import 'angular-breadcrumb'
import 'angular-material';
// Import angular
import 'angular/angular.js';
// Material design css
import 'angular-material/angular-material.css';
import './scss/vendor.scss'
import './scss/index.scss'
import _ from 'lodash';
window._ = _;
window.angular = angular;


export let app = angular.module('skykitProvisioning', [
  uiRouter,
  'ngAnimate',
  '720kb.tooltips',
  'ngCookies',
  'ngSanitize',
  'restangular',
  'ui.bootstrap',
  'ngMaterialDatePicker',
  'hSweetAlert',
  'ncy-angular-breadcrumb',
  'directive.g+signin',
  'ngProgress',
  'ngMaterial',
  'ngclipboard',
  'toastr',
  'lfNgMdFileInput'
])
