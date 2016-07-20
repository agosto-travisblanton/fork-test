describe('ProgressBarService', function () {
  let ProgressBarService = undefined;
  let ngProgressFactory = undefined;

  beforeEach(module('skykitProvisioning'));

  beforeEach(inject(function (_ProgressBarService_, _ngProgressFactory_) {
    ProgressBarService = _ProgressBarService_;
    return ngProgressFactory = _ngProgressFactory_;
  }));


  describe('constructor', () =>
    it('creates an instance of progress bar', () => expect(ProgressBarService.progressBar).toBeDefined())
  );


  describe('.start', function () {
    it('sets the progress bar\'s color', function () {
      spyOn(ProgressBarService.progressBar, 'setColor').and.callThrough();
      ProgressBarService.start();
      return expect(ProgressBarService.progressBar.setColor).toHaveBeenCalledWith('#00FCFF');
    });

    it('sets the progress bar\'s height', function () {
      spyOn(ProgressBarService.progressBar, 'setHeight').and.callThrough();
      ProgressBarService.start();
      return expect(ProgressBarService.progressBar.setHeight).toHaveBeenCalledWith('4px');
    });

    return it('starts the progress bar animation', function () {
      spyOn(ProgressBarService.progressBar, 'start').and.callThrough();
      ProgressBarService.start();
      return expect(ProgressBarService.progressBar.start).toHaveBeenCalled();
    });
  });


  return describe('.complete', () =>
    it('complete the progress bar animation', function () {
      spyOn(ProgressBarService.progressBar, 'complete').and.callThrough();
      ProgressBarService.complete();
      return expect(ProgressBarService.progressBar.complete).toHaveBeenCalled();
    })
  );
});
