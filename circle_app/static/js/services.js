"use strict";

var module = angular.module("services", ['djangoRESTResources']);

module.factory('Circle', function (djResource) {
    var resource = djResource('/api/v1/circle/:key/ ', {key: '@key'});
    return resource;
});
