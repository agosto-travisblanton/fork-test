'use strict'

describe 'ProofOfPlayCtrl', ->
  $controller = undefined
  controller = undefined
  ProofPlayService = undefined
  promise = undefined
  $stateParams = undefined
  $state = undefined
  ToastsService = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _ProofPlayService_, _$state_, _ToastsService_) ->
    $controller = _$controller_
    ProofPlayService = _ProofPlayService_
    $state = _$state_
    ToastsService = _ToastsService_

    controller = $controller 'ProofOfPlayCtrl', {
      ProofPlayService: ProofPlayService,
      $stateParams: $stateParams,
      $state: $state,
      ToastsService: ToastsService
    }

  describe 'at the start', ->
    it 'tab dict values should equal', ->
      resource = {
        title: 'Resource Report',

      }
      expect(angular.equals(resource, controller.resource)).toBeTruthy()

  describe 'Service functionality', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(ProofPlayService, 'getAllTenants').and.returnValue promise

    it 'sets inner tenants from Proofplay Service', ->
      controller.initialize()
      output = {
        data: {
          tenants: ["one_tenant"]
        }
      }
      promise.resolve(output)
      expect(controller.tenants).toEqual(output.data.tenants)


    it 'sets tenant', ->
      controller.submitTenant('some_tenant')
      expect(angular.equals(controller.chosen_tenant, 'some_tenant')).toBeTruthy()
