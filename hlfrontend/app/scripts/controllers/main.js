'use strict';

/**
 * @ngdoc function
 * @name adminApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the adminApp
 */
angular.module('adminApp')
  .controller('MainCtrl', function ($scope, $http, $window, authService, $state) {
    $http.get('http://localhost:2000/devices')
      .then(function success() {
        console.log('data')
        alert('worked')
      })
      .catch(function error() {
        alert('bad')
        console.log(err)
      })







    $scope.login = function() {
      authService.login($scope.username, $scope.password)
       .success(function (data, status, headers, config) {
        $window.sessionStorage.token = data.token;
        $state.go('application');
      })
      .error(function (data, status, headers, config) {
        // Erase the token if the user fails to log in
        delete $window.sessionStorage.token;
        alert('wrong!')
      });
    }
  });
