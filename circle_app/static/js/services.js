"use strict";

var module = angular.module("services", ['djangoRESTResources']);

module.factory('Circle', ['djResource', function (djResource) {
    var resource = djResource('/api/v1/circles/current/ ');
    return resource;
}]);
