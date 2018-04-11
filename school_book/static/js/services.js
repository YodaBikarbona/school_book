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
            url:  `${API_ENDPOINT.url}/login`,
            method: 'POST',
            data: user
          }).then(function(resp){
            if(resp.data.user){
              //if(resp.data.user.role.role_name == 'admin'){
                if(resp.data.user.email == username && resp.data.token){
                  storeUserCredidentals(resp.data);
                  resolve(resp.data);
                }
              //}
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
      url:`${API_ENDPOINT.url}/roles`,
      method: 'GET'
    }).then(function(resp){
      callback(resp.data.role_list)
    }, function(resp){
      console.log(resp)
    })}

  this.getUsers = function(role, callback){
    $http({
      url: `${API_ENDPOINT.url}/users/${role}`,
      method: 'GET',
      data: role
    }).then(function(resp){
      callback(resp.data.user_list)
    }, function(resp){
      console.log(resp)
    })}

  this.getUser = function(user_id, callback){
    console.log(`${API_ENDPOINT.url}/users/${user_id}`)
    $http({
      url: `${API_ENDPOINT.url}/users/${user_id}`,
      method: 'GET',
      data: user_id
    }).then(function(resp){
      callback(resp.data.user_object)
    }, function(resp){
      console.log(resp.data)
    })}

  this.addUser = function(user, callback){
    $http({
      url: `${API_ENDPOINT.url}/users/add`,
      method: 'POST',
      data: user
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.editUser = function(user, callback){
    $http({
      url: `${API_ENDPOINT.url}/users/edit`,
      method: 'POST',
      data: user
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.changePassword = function(new_object){
    $http({
      url: `${API_ENDPOINT.url}/users/change_password`,
      method: 'POST',
      data: new_object
    }).then(function(resp){
    }, function(resp){
      console.log(resp.data)
    })}

    this.activateUser = function(user_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/users/activate`,
      method: 'POST',
      data: {'user_id': user_id}
    }).then(function(resp){
      callback(resp.data.user_object)
    }, function(resp){
      console.log(resp.data)
    })}

    this.deactivateUser = function(user_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/users/deactivate`,
      method: 'POST',
      data: {'user_id': user_id}
    }).then(function(resp){
      callback(resp.data.user_object)
    }, function(resp){
      console.log(resp.data)
    })}

    this.deleteUser = function(user_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/users/${user_id}`,
      method: 'DELETE',
      data: user_id
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.getSchoolYears = function(callback){
    $http({
      url: `${API_ENDPOINT.url}/school_year`,
      method: 'GET'
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.addSchoolYears = function(school_year, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_year/add`,
      method: 'POST',
      data: school_year
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.getSchoolClasses = function(school_year_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_year/${school_year_id}`,
      method: 'GET',
      data: school_year_id
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.addSchoolSubject = function(school_subject, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_subjects/add`,
      method: 'POST',
      data: school_subject
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.getSchoolSubject = function(callback){
    $http({
      url: `${API_ENDPOINT.url}/school_subjects`,
      method: 'GET'
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.uploadImage = function(user_id, image, callback){
    $http({
      url: `${API_ENDPOINT.url}/upload/user/${user_id}`,
      method: 'POST',
      data: image
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}


    this.addClass = function(new_class, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/add`,
      method: 'POST',
      data: new_class
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.addStudentToClass = function(student_list, class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/students/add`,
      method: 'POST',
      data: {student_list: student_list, 
        class_id: class_id}
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

    this.addSubjectToClass = function(subject_list, class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/school_subjects/add`,
      method: 'POST',
      data: {subject_list: subject_list, 
        class_id: class_id}
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.dropSubjectFromClass = function(subject_id, class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/school_subjects/drop`,
      method: 'POST',
      data: {subject_id: subject_id, 
        class_id: class_id}
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.getSubjectFromClass = function(class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/school_subjects/class/${class_id}`,
      method: 'GET'
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.dropStudentFromClass = function(student_id, class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/students/drop`,
      method: 'POST',
      data: {student_id: student_id, 
        class_id: class_id}
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.getStudentsFromClass = function(class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/students/class/${class_id}`,
      method: 'GET'
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

  this.getClass = function(class_id, callback){
    $http({
      url: `${API_ENDPOINT.url}/school_class/class/${class_id}`,
      method: 'GET'
    }).then(function(resp){
      callback(resp.data)
    }, function(resp){
      console.log(resp.data)
    })}

}])

.service('professorservice', ['$http','API_ENDPOINT','$q', function($http,API_ENDPOINT,$q){

  this.getAbsence = function(class_id, date, callback){
    $http({
      url: `${API_ENDPOINT.url}/absence/class/${class_id}`,
      method: 'POST',
      data: {date: date}
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