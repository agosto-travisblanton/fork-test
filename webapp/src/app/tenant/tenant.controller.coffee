'use strict'

appModule = angular.module('skykitProvisioning')

appModule.controller 'TenantCtrl',
  ($scope, $location, $log, $stateParams, TenantsService, DomainsService, DevicesService, DistributorsService, $state, sweet,
    ProgressBarService, $cookies, $mdDialog) ->

    $scope.selectedIndex = 0

    $scope.$watch 'selectedIndex', (current, old) ->
      switch current
        when 0
          $location.url '/view1'
        when 1
          $location.url '/view2'
        when 2
          $location.url '/view3'
        return

    @
