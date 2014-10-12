var module = angular.module('current_circle', ['services']);

module.controller("BasicController", ["$scope", 
    function($scope) {
      $scope.blafasel = "Hallo Smile";
      $scope.eineliste = ['uk', 'marvin', 'smile'];
    }
]);