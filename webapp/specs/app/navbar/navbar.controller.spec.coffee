'use strict'

describe 'NavbarCtrl', ->
  $controller = undefined
  VersionService = undefined
  versionPromise = undefined

  beforeEach module('skykitDisplayDeviceManagement')

  beforeEach inject (_$controller_, _VersionService_) ->
    $controller = _$controller_
    VersionService = _VersionService_
    versionPromise = new skykitDisplayDeviceManagement.q.Mock

  it 'should call getVersion', ->
    version_service_spy = spyOn(VersionService, 'getVersion').and.returnValue(versionPromise)
    controller = $controller('NavbarCtrl', {VersionService: VersionService})
    expect(version_service_spy).toHaveBeenCalled()

  it 'should define the version name property', ->
    spyOn(VersionService, 'getVersion').and.returnValue(versionPromise)
    controller = $controller('NavbarCtrl', {VersionService: VersionService})
    version_name = 'Foobar'
    versionPromise.resolve({name: version_name})
    expect(controller.version.name).toBe(version_name)
