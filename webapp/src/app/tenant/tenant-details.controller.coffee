'use strict'

appModule = angular.module('skykitDisplayDeviceManagement')

appModule.controller 'TenantDetailsCtrl', ($stateParams, TenantsService, $state) ->
  @currentTenant = {
    key: undefined,
    name: undefined,
    tenant_code: undefined,
    admin_email: undefined,
    content_server_url: undefined,
    chrome_device_domain: undefined,
    active: true
  }

  @editMode = !!$stateParams.tenantKey

  if @editMode
    promise = TenantsService.getTenantByKey($stateParams.tenantKey)
    promise.then (data) =>
      @currentTenant = data

  @onClickSaveButton = () ->
    promise = TenantsService.save @currentTenant
    promise.then (data) ->
      $state.go 'tenants'

  @autoGenerateTenantCode = ->
    unless @currentTenant.key
      newTenantCode = ''
      if @currentTenant.name
        newTenantCode = @currentTenant.name.toLowerCase()
      @currentTenant.tenant_code = newTenantCode

  @
