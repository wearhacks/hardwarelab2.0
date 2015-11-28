'use strict';

/**
 * @ngdoc service
 * @name adminApp.authService
 * @description
 * # authService
 * Service in the adminApp.
 */
angular.module('adminApp')
  .service('authService', function ($http, $window, $q) {
    // AngularJS will instantiate a singleton by calling "new" on this function
    this.login = function login(username, password) {
      var data = {username: username, password: password}
      return $http.post('http://localhost:2000/admin/login', data);
    }
  });
