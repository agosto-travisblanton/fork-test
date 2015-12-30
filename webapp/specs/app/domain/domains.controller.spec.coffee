'use strict'

describe 'DomainsCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  DomainsService = undefined
  sweet = undefined
  promise = undefined


  beforeEach module('skykitProvisioning')

  beforeEach inject (_$controller_, _DomainsService_, _$state_, _sweet_) ->
    $controller = _$controller_
    $state = _$state_
    DomainsService = _DomainsService_
    sweet = _sweet_
    controller = $controller 'DomainsCtrl', {$state: $state, DomainsService: DomainsService, sweet: sweet}

  describe 'initialization', ->
    it 'domains should be an empty array', ->
      expect(angular.isArray(controller.domains)).toBeTruthy()

  describe '.initialize', ->
    domains = [
      {
        key: 'ahjad897d987fadafg708fg71',
        name: 'bob.agosto.com',
        impersonation_admin_email_address: 'bob.macneal@skykit.com',
        created: '2015-09-08 12:15:08',
        updated: '2015-09-08 12:15:08'
      }
      {
        key: 'bhjad897d987fadafg708y672',
        name: 'chris.agosto.com',
        impersonation_admin_email_address: 'chris.bartling@skykit.com',
        created: '2015-09-08 12:15:09',
        updated: '2015-09-08 12:15:09'
      }
      {
        key: 'chjad897d987fadafg708hb53',
        name: 'paul.agosto.com',
        impersonation_admin_email_address: 'paul.lundberg@skykit.com',
        created: '2015-09-08 12:15:10',
        updated: '2015-09-08 12:15:10'
      }
    ]

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(DomainsService, 'fetchAllDomains').and.returnValue promise

    it 'call DomainsService.fetchAllDomains to retrieve all domains', ->
      controller.initialize()
      promise.resolve domains
      expect(DomainsService.fetchAllDomains).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved domains in the controller", ->
      controller.initialize()
      promise.resolve domains
      expect(controller.domains).toBe domains

  describe '.editItem', ->
    domain = {key: 'ahjad897d987fadafg708fg71'}

    beforeEach ->
      spyOn $state, 'go'

    it "route to the 'editDomain' named route, passing the supplied domain key", ->
      controller.editItem(domain)
      expect($state.go).toHaveBeenCalledWith 'editDomain', {domainKey: domain.key}

  describe '.deleteItem', ->
    domain = {
      key: 'ahjad897d987fadafg708fg71'
      name: 'bob.agosto.com',
      created: '2015-05-10 22:15:10'
      updated: '2015-05-10 22:15:10'
    }

    beforeEach ->
      promise = new skykitProvisioning.q.Mock
      spyOn(DomainsService, 'delete').and.returnValue promise
      spyOn controller, 'initialize'
      spyOn(sweet, 'show').and.callFake (options, callback) ->
        callback()

    it 'call DomainsService.delete domain', ->
      controller.deleteItem domain
      promise.resolve()
      expect(DomainsService.delete).toHaveBeenCalledWith domain

    it "the 'then' handler calls initialize to re-fetch all domains", ->
      controller.deleteItem domain
      promise.resolve()
      expect(controller.initialize).toHaveBeenCalled

    it "the SweetAlert confirmation should be shown", ->
      controller.deleteItem domain
      promise.resolve()
      expect(sweet.show).toHaveBeenCalled

