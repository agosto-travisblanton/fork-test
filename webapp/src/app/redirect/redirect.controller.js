function RedirectCtrl(SessionsService, $state, $timeout) {
  "ngInject";

  let vm = this;

  SessionsService.removeUserInfo();

  $timeout(function () {
    $state.go('sign_in')
  }, 8000)


  return vm;
}
export {RedirectCtrl}
