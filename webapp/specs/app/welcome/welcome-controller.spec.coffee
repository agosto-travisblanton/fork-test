'use strict'

describe 'WelcomeCtrl', ->
  $controller = undefined
  controller = undefined
  $state = undefined
  DistributorsService = undefined
  promise = undefined
  identity = {OAUTH_CLIENT_ID: 'CLIENT-ID', STATE: 'STATE'}
  $rootScope = undefined
  $scope = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _$state_, _$rootScope_, _DistributorsService_) ->
    $controller = _$controller_
    $state = _$state_
    $rootScope = _$rootScope_
    $scope = _$rootScope_.$new()
    DistributorsService = _DistributorsService_
    spyOn($scope, '$on')
    controller = $controller 'WelcomeCtrl', {
      $state: $state
      $scope: $scope
      DistributorsService: DistributorsService
      identity: identity
    }


  describe 'initialization', ->
    it 'currentDistributor is undefined', ->
      expect(controller.currentDistributor).toBeUndefined()

    it 'distributors should be an empty array', ->
      expect(angular.isArray(controller.distributors)).toBeTruthy()

    it "add listener for 'event:google-plus-signin-success' event", ->
      expect($scope.$on).toHaveBeenCalledWith 'event:google-plus-signin-success', jasmine.any(Function)

    it "add listener for 'event:google-plus-signin-failure' event", ->
      expect($scope.$on).toHaveBeenCalledWith 'event:google-plus-signin-failure', jasmine.any(Function)


  describe '.initialize', ->
    distributors = [
      {
        key: 'dhjad897d987fadafg708fg7d',
        name: 'Agosto, Inc.',
        created: '2015-05-10 22:15:10',
        updated: '2015-05-10 22:15:10'
      }
      {
        key: 'dhjad897d987fadafg708y67d',
        name: 'Tierney Bros., Inc.',
        created: '2015-05-10 22:15:10',
        updated: '2015-05-10 22:15:10'
      }
    ]

    beforeEach ->
      promise = new skykitDisplayDeviceManagement.q.Mock
      spyOn(DistributorsService, 'fetchAll').and.returnValue promise
      controller.initialize()
      promise.resolve distributors

    it 'call DistributorsService.fetchAll() to retrieve all distributors', ->
      expect(DistributorsService.fetchAll).toHaveBeenCalled()

    it "the 'then' handler caches the retrieved distributors in the controller", ->
      expect(controller.distributors).toBe distributors

    it 'sets the clientId property on the controller', ->
      expect(controller.clientId).toBe identity.WEB_APP_CLIENT_ID

    it 'sets the state property on the controller', ->
      expect(controller.state).toBe identity.STATE


  describe '.selectDistributor', ->
    distributor = {
      key: 'dhjad897d987fadafg708fg7d',
      name: 'Agosto, Inc.',
      created: '2015-05-10 22:15:10',
      updated: '2015-05-10 22:15:10'
    }

    beforeEach ->
      controller.currentDistributor = distributor

    it 'sets the current distributor on the DistributorsService', ->
      controller.selectDistributor()
      expect(DistributorsService.currentDistributor).toBe distributor


# Stormpath success result:
#
#      {
#      "data": {"message": "Successful Login"},
#      "status": 200,
#      "config": {
#        "method": "POST",
#        "transformRequest": [null],
#        "transformResponse": [null],
#        "url": "/login",
#        "data": {
#          "access_token": "ya29.6AEU-1gykCwqRn-hnUWhYduy8nJ27TyZTEpxwXJFavFywHQc9xKn-K665Av9VsTOwQqipg",
#          "authuser": "0",
#          "client_id": "390010375778-gidaqujfhgkqrc5lat9t890mhc0nhutt.apps.googleusercontent.com",
#          "code": "4/iZvBQwOp-evsEfvHNoKIQLfjnB_o-dA0vTtPZsH_P6Q",
#          "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE1OGVkZTMwYzQzZTVhOGEyMDQ3ZGNhZGQwMWViNWY2YmMzYjI3MmIifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXRfaGFzaCI6InNqeVpyQWpGUE5SZnhzVHNQcVpCR2ciLCJhdWQiOiIzOTAwMTAzNzU3NzgtZ2lkYXF1amZoZ2txcmM1bGF0OXQ4OTBtaGMwbmh1dHQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJjX2hhc2giOiI0LVVEblFKWEZRU3pkeWRVVVc5Z3lnIiwic3ViIjoiMTAzNDczODUzMjQ4ODA3ODA2MjkxIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjM5MDAxMDM3NTc3OC1naWRhcXVqZmhna3FyYzVsYXQ5dDg5MG1oYzBuaHV0dC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImhkIjoiYWdvc3RvLmNvbSIsImVtYWlsIjoiQ2hyaXMuQmFydGxpbmdAYWdvc3RvLmNvbSIsImlhdCI6MTQ0MTc0NjAxNSwiZXhwIjoxNDQxNzQ5NjE1fQ.oP8fCa4Pgvi_HSNfMGf1oVZmNqtJDGgPuyXc3T6Hd14NkLFspkf76jwPzacC19tuvKERMuR0GAq-ByUj7U8epeEFABZjU09sYJBmZz04hs3_1zj5s1R-axzbGqM-m_DYBEGrN2mIVX9rS_Cb54KOh7cbPSjdfjyAnAlqSzn-iFFgFSfNmb7I_x9nGwD1HzIg1RIATzCUARJWlVDOJbr5ZN-cwQUinug5lyx5Dlqz1wugJGnceVEsmy6Khn7K_cnq3_sVo2jM5FGukeEYnf8m58KI23ZYfQP6GNGLKMM5gaw-5wBC5JADwRnnnO6tGHLJA2PPu3Q07oeOyLvgN8-n-A",
#          "scope": "https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/plus.moments.write https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/plus.profile.agerange.read https://www.googleapis.com/auth/plus.profile.language.read https://www.googleapis.com/auth/plus.circles.members.read",
#          "session_state": "769eedf867033bc57704e4b8ca7ad6ebb4e49f34..4315",
#          "state": "88NSVOR0BBK3JE07TTQFIOY7XTA6MPU4",
#          "status": {"google_logged_in": true, "signed_in": true, "method": "AUTO"}
#        },
#        "headers": {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json;charset=utf-8"}
#      },
#      "statusText": "OK"
#      }
