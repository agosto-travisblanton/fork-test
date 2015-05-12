window.skykitDisplayDeviceManagement ||= {}
window.skykitDisplayDeviceManagement.q ||= {}

class window.skykitDisplayDeviceManagement.q.Mock

  then: (@resolveFunc, @rejectFunc) ->

  resolve: (args) ->
    @resolveFunc(args)

  reject: (args) ->
    @rejectFunc(args)
