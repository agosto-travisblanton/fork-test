export default class ImageService {

  constructor(Restangular, SessionsService) {
    'ngInject';
    this.Restangular = Restangular;
    this.SessionsService = SessionsService;
  }

  getImages(tenant_urlsafe_key) {
    return this.Restangular.oneUrl('image', `/internal/v1/image/tenant/${tenant_urlsafe_key}`).getList()
  }

  saveImage(tenant_urlsafe_key, formData) {
    // jQuery ajax used here instead of angular / Restangular due to angular bug with posting form data
    return $.ajax({
      type: "POST",
      url: `/internal/v1/image/tenant/${tenant_urlsafe_key}`,
      data: formData,
      processData: false,
      contentType: false
    });
  }

  deleteImage(image_urlsafe_key) {
    let promise = this.Restangular.oneUrl('image', `/internal/v1/image/${image_urlsafe_key}`).remove();
    return promise;
  }


}


