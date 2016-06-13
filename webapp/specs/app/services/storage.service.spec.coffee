'use strict'

describe 'StorageService', ->
  beforeEach module 'skykitProvisioning'
  StorageService = undefined
  key = undefined 
  value = undefined

  beforeEach inject (_StorageService_) ->
    StorageService = _StorageService_
    key = "jim"
    value = "dwight"

  describe 'StorageService API', ->
    it 'sets then gets a value for a key', ->
      StorageService.set(key, value)
      expect(StorageService.get(key)).toEqual value
      
    it 'sets than does not get a value for key after removal of key', ->
      StorageService.set(key, value)
      StorageService.rm(key)
      expect(StorageService.get(key)).toEqual undefined
  
    it 'sets than does not get a value for key after removeAll', ->
      StorageService.set(key, value)
      pam = "pam"
      StorageService.set(pam, "angela")
      StorageService.removeAll()
      expect(StorageService.get(key)).toEqual undefined
      expect(StorageService.get(pam)).toEqual undefined
      