(function() {
  'use strict';
  var app;

  app = angular.module('skykitProvisioning');

  app.config(function(toastrConfig) {
    return angular.extend(toastrConfig, {
      progressBar: true,
      closeButton: true,
      tapToDismiss: true,
      newestOnTop: true,
      positionClass: 'toast-bottom-left',
      timeOut: 5000
    });
  });

  app.config(function($breadcrumbProvider) {
    return $breadcrumbProvider.setOptions({
      prefixStateName: 'home',
      template: 'bootstrap3'
    });
  });

}).call(this);

//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImluZGV4LWNvbmZpZy5jb2ZmZWUiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFBQTtBQUFBLE1BQUE7O0VBRUEsR0FBQSxHQUFNLE9BQU8sQ0FBQyxNQUFSLENBQWUsb0JBQWY7O0VBRU4sR0FBRyxDQUFDLE1BQUosQ0FBVyxTQUFDLFlBQUQ7V0FDVCxPQUFPLENBQUMsTUFBUixDQUFlLFlBQWYsRUFBNkI7TUFDM0IsV0FBQSxFQUFhLElBRGM7TUFFM0IsV0FBQSxFQUFhLElBRmM7TUFHM0IsWUFBQSxFQUFjLElBSGE7TUFJM0IsV0FBQSxFQUFhLElBSmM7TUFLM0IsYUFBQSxFQUFlLG1CQUxZO01BTTNCLE9BQUEsRUFBUyxJQU5rQjtLQUE3QjtFQURTLENBQVg7O0VBVUEsR0FBRyxDQUFDLE1BQUosQ0FBVyxTQUFDLG1CQUFEO1dBQ1QsbUJBQW1CLENBQUMsVUFBcEIsQ0FBK0I7TUFDN0IsZUFBQSxFQUFpQixNQURZO01BRTdCLFFBQUEsRUFBVSxZQUZtQjtLQUEvQjtFQURTLENBQVg7QUFkQSIsImZpbGUiOiJpbmRleC1jb25maWcuanMiLCJzb3VyY2VSb290IjoiL3NvdXJjZS8iLCJzb3VyY2VzQ29udGVudCI6WyIndXNlIHN0cmljdCdcblxuYXBwID0gYW5ndWxhci5tb2R1bGUgJ3NreWtpdFByb3Zpc2lvbmluZydcblxuYXBwLmNvbmZpZyAodG9hc3RyQ29uZmlnKSAtPlxuICBhbmd1bGFyLmV4dGVuZCB0b2FzdHJDb25maWcsIHtcbiAgICBwcm9ncmVzc0JhcjogdHJ1ZVxuICAgIGNsb3NlQnV0dG9uOiB0cnVlXG4gICAgdGFwVG9EaXNtaXNzOiB0cnVlXG4gICAgbmV3ZXN0T25Ub3A6IHRydWVcbiAgICBwb3NpdGlvbkNsYXNzOiAndG9hc3QtYm90dG9tLWxlZnQnXG4gICAgdGltZU91dDogNTAwMFxuICB9XG5cbmFwcC5jb25maWcgKCRicmVhZGNydW1iUHJvdmlkZXIpIC0+XG4gICRicmVhZGNydW1iUHJvdmlkZXIuc2V0T3B0aW9ucyB7XG4gICAgcHJlZml4U3RhdGVOYW1lOiAnaG9tZScsXG4gICAgdGVtcGxhdGU6ICdib290c3RyYXAzJ1xuICB9XG4iXX0=