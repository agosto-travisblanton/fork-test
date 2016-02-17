'use strict'

describe 'ProofOfPlayCtrl', ->
  $controller = undefined
  controller = undefined
  ProofPlayService = undefined
  promise = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _ProofPlayService_) ->
    $controller = _$controller_
    ProofPlayService = _ProofPlayService_

    controller = $controller 'ProofOfPlayCtrl', {ProofPlayService: ProofPlayService}

  describe 'at the start', ->
    it 'tab dict values should equal', ->
      resource = {
        title: 'Resource',

      }
      expect(angular.equals(resource, controller.resource)).toBeTruthy()

  describe 'Service functionality', ->
    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(ProofPlayService, 'getAllTenants').and.returnValue promise
      spyOn(ProofPlayService, 'setTenant').and.returnValue true

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
      expect(ProofPlayService.setTenant).toHaveBeenCalled()
