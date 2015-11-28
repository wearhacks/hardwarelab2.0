'use strict';

/**
 * @ngdoc overview
 * @name adminApp
 * @description
 * # adminApp
 *
 * Main module of the application.
 */
angular
  .module('adminApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.router'
  ])
  .config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $stateProvider
      .state('login', {
        url: '/',
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .state('application', {
        url: '/views/application',
        templateUrl: 'views/application.html',
        controller: 'AppCtrl',
        resolve: {
          user: function($http, $window, $q) {
          // Check if token exists, and if it does make sure it's correct
          var token = $window.sessionStorage.token 
          var data = {token: token}
          
          return $http.post('http://localhost:2000/admin/checkauth', data)
            .then(function success(res) {
              console.log(data)
              if (res.status === 200) {
                return $q.when();
              } else {
                return $state.go('login')
              }
            })
        }}
      });
    $locationProvider.html5Mode(true);
  });
