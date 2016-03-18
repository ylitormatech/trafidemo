/**
 * Created by marco on 9.3.2016.
 */
trafiApp = angular.module('trafiApp', ['ngRoute']);

trafiApp.config(['$routeProvider',
    function($routeProvider) {
      $routeProvider.
          when('/municipals/', {
            templateUrl: 'static/templates/angular1demo/municipals.html',
            controller: 'MunicipalListController'
      }).
          when('/municipals/:municipal/', {
              templateUrl: 'static/templates/angular1demo/municipal-view.html',
              controller: 'MunicipalViewController'
      }).
          when('/municipals/:municipal/:year/', {
              templateUrl: 'static/templates/angular1demo/municipal-view.html',
              controller: 'MunicipalYearViewController'
      }).
          otherwise({
              redirectTo: '/municipals/'
      })
    }]);
/** change notation so Angula and Jinja2 can co-exist at same template
 * angular notation should be written e.g. {a value a}
 */
trafiApp.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

trafiApp.factory('municipals', function($http){
  return {
    list: function(callback){
      $http.get('/api/trafi/').success(callback);
    },
    find: function(name, callback){
      $http.get('/municipals/:id/').success(function(data){
        var municipal = data.filter(function(entry){
          return entry.kunta = name;
        })[0];
        callback(municipal);
      })
    }
  }
});
var xx;
trafiApp.controller('MunicipalListController', function($scope, $http, municipals){

   municipals.list(function(municipals){
       $scope.municipals = municipals.data;
   });

});