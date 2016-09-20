import Lockr from 'lockr';

export default class StorageService {

  constructor() {
  }

  set(key, value) {
    return Lockr.set(key, value);
  }

  get(key) {
    return Lockr.get(key);
  }

  rm(key) {
    return Lockr.rm(key);
  }

  removeAll() {
    Lockr.flush();
  }

}

