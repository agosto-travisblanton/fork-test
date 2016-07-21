export default class ProofPlayService {

  constructor($http,
              $q,
              $window,
              SessionsService,
              $stateParams,
              $state,
              ToastsService) {
    this.$http = $http
    this.$q = $q
    this.$window = $window
    this.SessionsService = SessionsService
    this.$stateParams = $stateParams
    this.$state = $state
    this.ToastsService = ToastsService
    this.makeHTTPRequest = this.makeHTTPRequest.bind(this);
    this.uriBase = 'proofplay/api/v1';
  }

  makeHTTPURL(where_to_go, tenant) {
    return this.uriBase + where_to_go + tenant;
  }

  makeHTTPRequest(where_to_go, tenant) {
    let deferred = this.$q.defer();
    let url = this.makeHTTPURL(where_to_go, tenant);
    return this.$http.get(url);
  }

  getAllResources(tenant) {
    let r = this.makeHTTPRequest("/retrieve_all_resources/", tenant);
    // the catch is only done here because 3 proof of play views are initilized at the same time
    // so this catch will be done 3 times with 3 error messages if we add it to getAllDisplays and getAllLocations
    r.catch(function (err, data) {
      let {status} = err;
      if (status === 403) {
        this.ToastsService.showErrorToast("You are not allowed to view this tenant!");
        this.$state.go('proof', {});
      }
      if (status === 404) {
        this.ToastsService.showErrorToast("You must select a tenant first!");
        return this.$state.go('proof', {});
      }
    });

    return r.then(data => data);
  }


  getAllDisplays(tenant) {
    return this.makeHTTPRequest("/retrieve_all_displays/", tenant);
  }


  getAllLocations(tenant) {
    return this.makeHTTPRequest("/retrieve_all_locations/", tenant);
  }


  getAllTenants() {
    return this.makeHTTPRequest("/retrieve_my_tenants", '');
  }


  downloadCSVForMultipleResourcesByDate(start_date, end_date, resources, tenant) {
    let allResources = '';

    for (let i = 0; i < resources.length; i++) {
      let each = resources[i];
      allResources = allResources + "|" + each;
    }

    this.$window.open(this.uriBase + '/multi_resource_by_date/' + start_date + '/' + end_date + '/' + allResources + '/' +
      tenant + "/" + this.SessionsService.getCurrentDistributorKey()

      , '_blank');
    return true;
  }


  downloadCSVForMultipleResourcesByDevice(start_date, end_date, resources, tenant) {
    let allResources = '';

    for (let i = 0; i < resources.length; i++) {
      let each = resources[i];
      allResources = allResources + "|" + each;
    }

    this.$window.open(this.uriBase + '/multi_resource_by_device/' + start_date + '/' + end_date + '/' + allResources + '/' +
      tenant + "/" + this.SessionsService.getCurrentDistributorKey()
      , '_blank');
    return true;
  }


  downloadCSVForMultipleDevicesSummarized(start_date, end_date, devices, tenant) {
    let allDevices = '';

    for (let i = 0; i < devices.length; i++) {
      let each = devices[i];
      allDevices = allDevices + "|" + each;
    }

    this.$window.open(this.uriBase + '/multi_device_summarized/' + start_date + '/' + end_date + '/' + allDevices + '/' +
      tenant + "/" + this.SessionsService.getCurrentDistributorKey()
      , '_blank');
    return true;
  }


  downloadCSVForMultipleDevicesByDate(start_date, end_date, devices, tenant) {
    let allDevices = '';

    for (let i = 0; i < devices.length; i++) {
      let each = devices[i];
      allDevices = allDevices + "|" + each;
    }

    this.$window.open(this.uriBase + '/multi_device_by_date/' + start_date + '/' + end_date + '/' + allDevices + '/' +
      tenant + "/" + this.SessionsService.getCurrentDistributorKey()
      , '_blank');
    return true;
  }

  downloadCSVForMultipleLocationsByDevice(start_date, end_date, locations, tenant) {
    let allLocations = '';

    for (let i = 0; i < locations.length; i++) {
      let each = locations[i];
      allLocations = allLocations + "|" + each;
    }

    this.$window.open(this.uriBase + '/multi_location_by_device/' + start_date + '/' + end_date + '/' + allLocations + '/' +
      tenant + "/" + this.SessionsService.getCurrentDistributorKey()
      , '_blank');
    return true;
  }

  downloadCSVForMultipleLocationsSummarized(start_date, end_date, locations, tenant) {
    let allLocations = '';

    for (let i = 0; i < locations.length; i++) {
      let each = locations[i];
      allLocations = allLocations + "|" + each;
    }

    this.$window.open(this.uriBase + '/multi_location_summarized/' + start_date + '/' + end_date + '/' + allLocations + '/' +
      tenant + "/" + this.SessionsService.getCurrentDistributorKey()
      , '_blank');
    return true;
  }


  createFilterFor(query) {
    query = angular.lowercase(query);
    return function (resource) {
      resource = angular.lowercase(resource);
      return (resource.indexOf(query) === 0);
    };
  }


  querySearch(resources, searchText) {
    if (searchText) {
      return resources.filter(this.createFilterFor(searchText));
    } else {
      return resources;
    }
  }


}

ProofPlayService.$inject = [
  "$http", "$q", "$window", "SessionsService", "$stateParams", "$state", "ToastsService",
]
