import localStorage from 'local-storage';

export default class StorageService {

  constructor() {
  }

  set(key, value) {
    return localStorage.set(key, value);
  }

  get(key) {
    return localStorage.get(key);
  }

  rm(key) {
    return localStorage.remove(key);
  }

  removeAll() {
    localStorage.clear();
  }
  
}

