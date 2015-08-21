'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'TenantDetailsCtrl', ($stateParams, TenantsService, DevicesService, $state) ->
  @currentTenant = {
    key: undefined,
    name: undefined,
    tenant_code: undefined,
    admin_email: undefined,
    content_server_url: undefined,
    chrome_device_domain: undefined,
    active: true
  }

  @currentTenantDisplays = []
  @editMode = !!$stateParams.tenantKey

  if @editMode
    tenantPromise = TenantsService.getTenantByKey($stateParams.tenantKey)
    tenantPromise.then (data) =>
      @currentTenant = data

    displaysPromise = DevicesService.getDevicesByTenant($stateParams.tenantKey)
    displaysPromise.then (data) =>
      @currentTenantDisplays = data.objects

  @onClickSaveButton = () ->
    promise = TenantsService.save @currentTenant
    promise.then () ->
      $state.go 'tenants'

  @editItem = (item) ->
    $state.go 'editDevice', {deviceKey: item.key, tenantKey: $stateParams.tenantKey}

  @autoGenerateTenantCode = ->
    unless @currentTenant.key
      newTenantCode = ''
      if @currentTenant.name
        newTenantCode = @currentTenant.name.toLowerCase()
        newTenantCode = newTenantCode.replace(/\s+/g, '_')
        newTenantCode = newTenantCode.replace(/\W+/g, '')
      @currentTenant.tenant_code = newTenantCode

  @
