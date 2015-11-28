'use strict';

/**
 * @ngdoc function
 * @name adminApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the adminApp
 */
angular.module('adminApp')
  .controller('AppCtrl', function ($scope, $window, $http) {
  	$scope.name = 'asdfads'
  	if (!$window.sessionStorage.token) {
  		alert('You not authd');
  	} else {
  		$http.get('http://localhost:2000/admin/get_application')
  			.then(function success(res) {
  				$scope.data = res.data[0]
  				$scope.social = JSON.parse(res.data[0].social)
  				$scope.extraQuestions = JSON.parse(res.data[0].extraQuestions)

  			})
  	}

  	$scope.accept = function() {

  	}
  	$scope.maybe = function() {

  	}
  	$scope.deny = function() {

  	}

  });
