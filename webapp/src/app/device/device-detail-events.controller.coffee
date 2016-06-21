'use strict'
appModule = angular.module('skykitProvisioning')
appModule.controller 'DeviceDetailsEventsCtrl', (
  $log,
  $stateParams,
  $state,
  SessionsService,
  DevicesService,
  LocationsService,
  CommandsService,
  TimezonesService,
  sweet,
  ProgressBarService,
  $mdDialog,
  ToastsService) ->
    vm = @
    vm.tenantKey = $stateParams.tenantKey
    vm.deviceKey = $stateParams.deviceKey
    vm.fromDevices = $stateParams.fromDevices is "true"
    vm.currentDevice = {}
    vm.dayRange = 30
    vm.issues = []
    vm.pickerOptions = "{widgetPositioning: {vertical:'bottom'}, showTodayButton: true, sideBySide: true, icons:{
              next:'glyphicon glyphicon-arrow-right',
              previous:'glyphicon glyphicon-arrow-left',
              up:'glyphicon glyphicon-arrow-up',
              down:'glyphicon glyphicon-arrow-down'}}"

    now = new Date()
    today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    vm.endTime = now.toLocaleString().replace(/,/g, "")
    today.setDate(now.getDate() - vm.dayRange)
    vm.startTime = today.toLocaleString().replace(/,/g, "")
    
    vm.generateLocalFromUTC = (UTCTime) ->
      localTime = moment.utc(UTCTime).toDate()
      localTime = moment(localTime).format('YYYY-MM-DD hh:mm:ss A')

    vm.replaceIssueTime = (issues) ->
      for each in issues
        if each.created
          each.created = vm.generateLocalFromUTC(each.created)
        if each.updated
          each.updated = vm.generateLocalFromUTC(each.updated)

    vm.replaceCommandTime = (issues) ->
      for each in issues
        if each.postedTime
          each.postedTime = vm.generateLocalFromUTC(each.postedTime)
        if each.confirmedTime
          each.confirmedTime = vm.generateLocalFromUTC(each.confirmedTime)

    vm.getIssues = (device, epochStart, epochEnd, prev, next) ->
      ProgressBarService.start()
      issuesPromise = DevicesService.getIssuesByKey(device, epochStart, epochEnd, prev, next)
      issuesPromise.then (data) ->
        vm.replaceIssueTime(data.issues)
        vm.issues = data.issues
        vm.prev_cursor = data.prev
        vm.next_cursor = data.next
        ProgressBarService.complete()

    vm.paginateCall = (forward) ->
      if forward
        vm.getIssues vm.deviceKey, vm.epochStart, vm.epochEnd, null, vm.next_cursor

      else
        vm.getIssues vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, null

    vm.initialize = () ->
      vm.epochStart = moment(new Date(vm.startTime)).unix()
      vm.epochEnd = moment(new Date(vm.endTime)).unix()

      devicePromise = DevicesService.getDeviceByKey vm.deviceKey
      devicePromise.then ((response) ->
        vm.onGetDeviceSuccess(response)
      ), (response) ->
        vm.onGetDeviceFailure(response)

      vm.getIssues vm.deviceKey, vm.epochStart, vm.epochEnd

    vm.onGetDeviceSuccess = (response) ->
      vm.currentDevice = response
      vm.selectedTimezone = response.timezone if response.timezone != vm.selectedTimezone
      vm.tenantKey = vm.currentDevice.tenantKey if vm.tenantKey is undefined
      if $stateParams.fromDevices is "true"
        vm.backUrl = '/#/devices'
        vm.backUrlText = 'Back to devices'
      else
        if vm.currentDevice.isUnmanagedDevice is true
          vm.backUrl = "/#/tenants/#{vm.tenantKey}/unmanaged"
          vm.backUrlText = 'Back to tenant unmanaged devices'
        else
          vm.backUrl = "/#/tenants/#{vm.tenantKey}/managed"
          vm.backUrlText = 'Back to tenant managed devices'

    vm.onGetDeviceFailure = (response) ->
      ToastsService.showErrorToast 'Oops. We were unable to fetch the details for this device at this time.'
      errorMessage = "No detail for device_key ##{vm.deviceKey}. Error: #{response.status} #{response.statusText}"
      $log.error errorMessage
      $state.go 'devices'
      
      
    vm.onClickRefreshButton = () ->
      ProgressBarService.start()
      vm.epochStart = moment(new Date(vm.startTime)).unix()
      vm.epochEnd = moment(new Date(vm.endTime)).unix()
      vm.prev_cursor = null
      vm.next_cursor = null
      issuesPromise = DevicesService.getIssuesByKey(vm.deviceKey, vm.epochStart, vm.epochEnd, vm.prev_cursor, vm.next_cursor)
      issuesPromise.then ((data) ->
        vm.onRefreshIssuesSuccess(data)
      ), (error) ->
        vm.onRefreshIssuesFailure(error)

    vm.onRefreshIssuesSuccess = (data) ->
      vm.replaceIssueTime(data.issues)
      vm.issues = data.issues
      vm.prev_cursor = data.prev
      vm.next_cursor = data.next
      ProgressBarService.complete()

    vm.onRefreshIssuesFailure = (error) ->
      ProgressBarService.complete()
      ToastsService.showInfoToast 'We were unable to refresh the device issues list at this time.'
      $log.error "Failure to refresh device issues: #{error.status } #{error.statusText}"


    vm

