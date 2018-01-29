angular.module('school_book')
.service('authservice', ['$http','API_ENDPOINT','$q', function($http,API_ENDPOINT,$q){
      var LOCAL_STORAGE_KEY = 'mytoken'
      var authToken;
      var isAuthenticated = false;
      var role = '';
      var userObj = {};

      function loadUserCredidentals(){
        var token = window.localStorage.getItem('mytoken')
          if(token){
            isAuthenticated = true;
             $http.defaults.headers.common['Authorization'] = token;
          }
      }

      function storeUserCredidentals(user){
        console.log(user)
        window.localStorage.setItem(LOCAL_STORAGE_KEY, user.token);
        window.localStorage.setItem('user', JSON.stringify(user))
        useUserCredidentals(user);

      }

      function useUserCredidentals(user){
        userObj = user;
        isAuthenticated = true;
        authToken = user.token;
        role = user.user.role.role_name;

        $http.defaults.headers.common['Authorization'] = authToken;

      }

      function destroyUserCredidentals(){
        isAuthenticated = false;
        userObj = {};
        role = '';
        window.localStorage.clear(LOCAL_STORAGE_KEY);
        window.localStorage.clear('user');
         $http.defaults.headers.common.Authorization = undefined;
        

      }

      var login = function(user){
        username = user.username
        return $q(function(resolve, reject){
          $http({
            url: 'http://localhost:6543/login',
            method: 'POST',
            data: user
          }).then(function(resp){
            console.log(resp)
            if(resp.data.user){
              if(resp.data.user.role.role_name == 'admin'){
                if(resp.data.user.email == username && resp.data.token){
                  storeUserCredidentals(resp.data);
                  resolve(resp.data);
                }
              }
            }
            else{
              reject(resp.data)
              console.log('Error')
            }
          }, function(resp){
            console.log(resp)
          })
        })


        /*return $q(function(resolve,reject){
                    $http({
                          url :     API_ENDPOINT.url + '/login',
                          method : 'POST',
                          data :    user
      }).then(function(resp){
          if(resp.data.status = 'Ok'){
            storeUserCredidentals(resp.data.user_data);
              resolve(resp.data);
          }else{
            reject(resp.data);
            
          }
        },function(resp){
          console.log(resp)
            
          });
  })*/}
        loadUserCredidentals();
      
      var logout = function(){
        destroyUserCredidentals();
      }

      return {
        login : login,
        logout : logout,
        isAuthorized : true,
        isAuthenticated : function(){return isAuthenticated;},
        userObj : function(){return userObj;},
        role: function(){return role;}
      }
  }])

/*.factory('AuthInterceptor', ['$rootScope', function($rootScope){
    var inter = {}
    
   return inter;
}])

.config(['$httpProvider',function($httpProvider) {
    $httpProvider.interceptors.push('AuthInterceptor');
}])*/