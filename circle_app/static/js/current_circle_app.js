var module = angular.module('current_circle', ['services']).config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
});

module.controller("BasicController", ["$scope", 'Circle',
    function($scope, Circle) {
      Circle.get({}, function(data){
        $scope.circle = data;
      });
      //$scope.eineliste = ['uk', 'marvin', 'smile'];
    }
]);
