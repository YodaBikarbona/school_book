angular.module('school_book')
.service('authservice', ['$http','API_ENDPOINT','$q', function($http,API_ENDPOINT,$q){
      var LOCAL_STORAGE_KEY = 'mytoken'
      var authToken;
      var isAuthenticated = false;
      var role = '';
      var userObj = {};
      var user_id;

      function loadUserCredidentals(){
        var token = window.localStorage.getItem('mytoken')
          if(token){
            isAuthenticated = true;
             $http.defaults.headers.common['Authorization'] = token;
          }
        user_id = window.localStorage.getItem('user_id')
      }

      function storeUserCredidentals(user){
        window.localStorage.setItem(LOCAL_STORAGE_KEY, user.token);
        window.localStorage.setItem('user_id', JSON.stringify(user.user.id))
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
        role: function(){return role;},
        user_id: function(){return user_id}
      }
  }])

.service('adminservice', ['$http','API_ENDPOINT','$q', function($http,API_ENDPOINT,$q){


  this.getRoles = function(callback){
    $http(
    {
      url:'http://localhost:6543/roles',
      method: 'GET'
    }).then(function(resp){
      callback(resp.data.role_list)
    }, function(resp){
      console.log(resp)
    })}

  this.getUsers = function(role, callback){
    $http({
      url: 'http://localhost:6543/users/'+role,
      method: 'GET',
      data: role
    }).then(function(resp){
      callback(resp.data.user_list)
    }, function(resp){
      console.log(resp)
    })}

  this.getUser = function(user_id, callback){
    $http({
      url: 'http://localhost:6543/users/'+user_id,
      method: 'GET',
      data: user_id
    }).then(function(resp){
      callback(resp.data.user_object)
    }, function(resp){
      console.log(resp.data)
    })}

  this.addUser = function(user, callback){
    $http({
      url: 'http://localhost:6543/users/add',
      method: 'POST',
      data: user
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.activateUser = function(user_id, callback){
    $http({
      url: 'http://localhost:6543/users/activate',
      method: 'POST',
      data: {'user_id': user_id}
    }).then(function(resp){
      callback(resp.data.user_object)
    }, function(resp){
      console.log(resp.data)
    })}

    this.deactivateUser = function(user_id, callback){
    $http({
      url: 'http://localhost:6543/users/deactivate',
      method: 'POST',
      data: {'user_id': user_id}
    }).then(function(resp){
      callback(resp.data.user_object)
    }, function(resp){
      console.log(resp.data)
    })}

    this.deleteUser = function(user_id, callback){
    $http({
      url: 'http://localhost:6543/users/'+user_id,
      method: 'DELETE',
      data: user_id
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

}])

/*.factory('AuthInterceptor', ['$rootScope', function($rootScope){
    var inter = {}
    
   return inter;
}])

.config(['$httpProvider',function($httpProvider) {
    $httpProvider.interceptors.push('AuthInterceptor');
}])*/