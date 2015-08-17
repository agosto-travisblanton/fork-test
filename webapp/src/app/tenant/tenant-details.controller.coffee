'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'TenantDetailsCtrl', ($stateParams, TenantsService, DevicesService, DisplaysService, $state) ->
  @currentTenant = {
    key: undefined,
    name: undefined,
    tenant_code: undefined,
    admin_email: undefined,
    content_server_url: undefined,
    chrome_device_domain: undefined,
    active: true
  }

  @currentTenantDevices = []
  @currentTenantDisplays = []
  @editMode = !!$stateParams.tenantKey

  if @editMode
    tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey)
    tenantPromise.then (data) =>
      @currentTenant = data

    devicesPromise = DevicesService.getDevicesByTenant($stateParams.tenantKey)
    devicesPromise.then (data) =>
      @currentTenantDevices = data

    displaysPromise = DisplaysService.getDisplaysByTenant($stateParams.tenantKey)
    displaysPromise.then (data) =>
      @currentTenantDisplays = data.objects

  @onClickSaveButton = () ->
    promise = TenantsService.save @currentTenant
    promise.then (data) ->
      $state.go 'tenants'

  @autoGenerateTenantCode = ->
    unless @currentTenant.key
      newTenantCode = ''
      if @currentTenant.name
        newTenantCode = @currentTenant.name.toLowerCase()
        newTenantCode = newTenantCode.replace(/\s+/g, '_')
        newTenantCode = newTenantCode.replace(/\W+/g, '')
      @currentTenant.tenant_code = newTenantCode

  @
