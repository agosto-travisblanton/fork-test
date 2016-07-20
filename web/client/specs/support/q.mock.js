if (!window.skykitProvisioning) {
  window.skykitProvisioning = {};
}
if (!window.skykitProvisioning.q) {
  window.skykitProvisioning.q = {};
}

window.skykitProvisioning.q.Mock = class Mock {

  then(resolveFunc, rejectFunc) {
    this.resolveFunc = resolveFunc;
    this.rejectFunc = rejectFunc;
    return;
  }

  resolve(args) {
    return this.resolveFunc(args);
  }

  reject(args) {
    return this.rejectFunc(args);
  }
};
