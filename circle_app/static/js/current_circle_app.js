var module = angular.module('current_circle', ['services']).config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
});

module.controller("BasicController", ["$scope", 'Circle',
    function($scope, Circle) {
      $scope.circle = Circle;
      $scope.blafasel = "Hallo Smile";
      $scope.eineliste = ['uk', 'marvin', 'smile'];
      $scope.double = function(value) { return value * 2; };

    }
]);
