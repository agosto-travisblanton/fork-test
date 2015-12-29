window.skyKitProvisioning ||= {}
window.skyKitProvisioning.q ||= {}

class window.skyKitProvisioning.q.Mock

  then: (@resolveFunc, @rejectFunc) ->

  resolve: (args) ->
    @resolveFunc(args)

  reject: (args) ->
    @rejectFunc(args)
