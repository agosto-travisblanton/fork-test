window.skykitProvisioning ||= {}
window.skykitProvisioning.q ||= {}

class window.skykitProvisioning.q.Mock

  then: (@resolveFunc, @rejectFunc) ->

  resolve: (args) ->
    @resolveFunc(args)

  reject: (args) ->
    @rejectFunc(args)
