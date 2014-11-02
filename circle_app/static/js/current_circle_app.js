var module = angular.module('current_circle', ['services', 'circleFilters']).config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{$');
      $interpolateProvider.endSymbol('$}');
});

module.controller("BasicController", ['$interval', 'Circle',
    function($interval, Circle) {
      var self = this;
      $interval(function(){
        Circle.get({}, function(data){
          self.circle = data;
        });
      }, 1000);
      //$scope.eineliste = ['uk', 'marvin', 'smile'];
    }
]);
