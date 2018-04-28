angular.module('school_book', ['ui.router', 'ui.bootstrap', 'ngSanitize'])

.directive('fileModel', ['$parse', function ($parse) {
     return {
         restrict: 'A',
         link: function(scope, element, attrs) {
             var model = $parse(attrs.fileModel);
             var modelSetter = model.assign;
 
             element.bind('change', function(){
                 scope.$apply(function(){
                     modelSetter(scope, element[0].files[0]);
                 });
             });
         }
     };
 }])

.config(['$stateProvider','$urlRouterProvider','STATES',function($stateProvider,$urlRouterProvider,STATE) {
	//Prvi nacin
	//$stateProvider.state('login', {
		//url:'/login',
		//templateUrl:'login.html',
		//controller: ime kontrolera za login i mora biti pod navnodnicima kao gore url npr controller: 'login'
	//})
	// Samo za rute koje nisu definirane da ih vrati na login
	//Drugi nacin
	$stateProvider
		.state(STATE.login)
		.state(STATE.admin)
        .state(STATE.professor)
		//.state('test',{url:'/test', templateUrl:'new_user.html'})
		.state(STATE.test)
	//Ovo za oba nacina treba
	$urlRouterProvider.otherwise('/login')
	
}])
//Ovo je za rute

/*.controller('loginController', ['$scope','$state','$http','$q', function($scope, $state, $http, $q){

	$scope.login = (user) => {
		username = user.username
		password = user.password
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
							$state.go('admin')
						}
					}
				}
				else{
					console.log('Error')
				}
			}, function(resp){
				console.log(resp)
			})
		})
		//if(login_data.data.user.email == username && 
		//	login_data.data.user.role.role_name == 'admin' && 
		//	login_data.data.user.token){
		//	$state.go('admin', {user:{
		//		username: username,
		//		password: password
		//	}})
		}
	//}
	
}])*/




.controller('loginController', ['$scope','authservice','$rootScope','$state', function($scope,auth,$rootScope,$state){

	$scope.login = (user) => {
		if (user) {
			auth.login(user).then(function(authenticated){
				if (auth.role() == 'admin') {
					$state.go('admin')
				}
                else if (auth.role() == 'professor') {
                    $state.go('professor')
                }
			}, function(err){

			})
		}

	}}])

.controller('mainController', ['$state','$scope','$rootScope','authservice',function($state,$scope,$rootScope,auth){
    $scope.logout = function(){
      auth.logout();
      $state.go('login')
    }
}])


.controller('adminController', ['$scope','$http','$q','$rootScope','adminservice','authservice', 'API_ENDPOINT', function($scope,$http,$q,$rootScope,adminservice,auth, API_ENDPOINT){
	$scope.show_tab = 0
	$scope.user_list_lenght = 0
	$scope.school_year_list_lenght = 0
    $scope.school_classes_lenght = 0
    $scope.school_subject_list_lenght = 0
    $scope.show_subtab = 0
    $scope.student_list = []
	$scope.userID = auth.user_id()
    let student_list_to_server = []
    let subject_list_to_server = []
	var temp_role = ''

	$scope.show_profile = function(){
		$scope.show_tab = 0
		$scope.disable_button = true
		var user_id = localStorage.getItem('user_id')
        $scope.getUser($scope.userID = user_id)
		$scope.show_tab = 1
		$scope.user_list_lenght = 0
        $scope.school_classes_lenght = 0
	}

	$scope.show_users = function(){
		$scope.show_tab = 0
        $scope.users = [];
        $scope.user_list_lenght = 0
		// Može se koristiti
		//$scope.user_list_lenght = 0
		$scope.getRoles()
		$scope.show_tab = 2
        $scope.school_classes_lenght = 0
	}

	$scope.find_by_role = function(role){
        $scope.school_subject_list_lenght = 0
        $scope.school_class_subject_view = 0
		temp_role = role
		$scope.getUsers(role)
	}

	$scope.show_classes = function(){
		$scope.show_tab = 0
        $scope.show_subtab = 0
        $scope.user_list_lenght = 0
        $scope.find_by_role("Professor")
		$scope.get_school_years()
		$scope.show_tab = 3
	}
	
    $scope.show_subjects = function(){
        $scope.show_tab = 0
        $scope.find_by_role("Professor")
        $scope.getSchoolSubject()
        $scope.show_tab = 4
    }


	$scope.lista = []
	for (var i = 0; i<50; i++) {
		$scope.lista.push(i)
	}

    $scope.getUsers = function(role){
        $scope.users = [];
        adminservice.getUsers(role,function(users){
            $scope.users = users;
            if($scope.users){
			$scope.user_list_lenght = $scope.users.length
		}
        });
      }

    $scope.addSchoolSucject = function(new_subject){
    }

    $scope.getRoles = function(){
        $scope.roles = [];
        adminservice.getRoles(function(roles){
            $scope.roles = roles;
        });
      }

    $scope.getUser = function(user_id){
    	$scope.user_obj = {}
    	adminservice.getUser(user_id, function(user_obj){
    		$scope.user_obj = user_obj;
            $scope.user_obj.edit_birth_date = new Date($scope.user_obj.birth_date)
    	})
    }

    $scope.change_tab = function(user_id){
    	$scope.show_tab = 0
    	$scope.disable_button = false
    	$scope.getUser(user_id)
    	$scope.show_tab = 1
    }

    $scope.addUser = function(user){
    	var date = new Date(user.birth_date)
  		date = date.setDate(date.getDate() + 1)
  		user.birth_date = new Date(date)
    	$scope.user_obj = {}
    	adminservice.addUser(user, function(user_obj){
    		$scope.user_obj = user_obj;
    	})
    }

    $scope.editUser = function(user){
        var date = new Date(user.edit_birth_date)
        date = date.setDate(date.getDate())
        user.birth_date = new Date(date)
        console.log(user.birth_date)
        adminservice.editUser(user, function(user_obj){
            $scope.user_obj = user_obj.user_obj;
            $scope.user_obj.edit_birth_date = new Date(user_obj.user_obj.birth_date)
        })
    }

    $scope.restart_form = function(){
    	$scope.new_user = {}
        $scope.new_subject = {}
        $scope.file = {}
        $scope.files = {}
        $scope.image = {}
        $scope.myFile = ""
        $scope.new_class = {}
        $scope.new_obj = {}
        $scope.new_object = {}
        $scope.user_list_lenght = 0
        $scope.school_subject_list_lenght = 0
        $scope.school_class_subject_view = 0
        var image_id = document.getElementById("inputImage")
        image_id.value = ''
    }

    $scope.activate_user = function(user_id){
    	adminservice.activateUser(user_id, function(user_obj){
    		$scope.user_obj.activated = user_obj.activated;
    	})
    	$scope.getUsers(temp_role)
    }

    $scope.deactivate_user = function(user_id){
    	adminservice.deactivateUser(user_id, function(user_obj){
    		$scope.user_obj.activated = user_obj.user_deactivated;
    	})
    	$scope.getUsers(temp_role)
    }

    $scope.delete_user = function(user_id){
    	$scope.show_tab = 0
    	adminservice.deleteUser(user_id, function(user_obj){
    	})
    	$scope.getUsers(temp_role)
    }

    $scope.get_school_years = function(){
    	$scope.school_years = []
    	adminservice.getSchoolYears(function(school_years){
    		$scope.school_years = school_years.school_year_list;
    		if ($scope.school_years) {
    			$scope.school_year_list_lenght = $scope.school_years.length
    		}
    	})
    }

    $scope.addSchoolYear = function(school_year){
    	$scope.school_year_obj = {}
    	adminservice.addSchoolYears(school_year, function(school_year_obj){
    		$scope.school_year_obj = school_year_obj;
    		$scope.get_school_years()
    	})
    }

    $scope.find_by_school_year_id = function(school_year_id){
    	$scope.getSchoolClasses(school_year_id)
    }
    
    $scope.getSchoolClasses = function(school_year_id){
    	$scope.school_classes = []
    	adminservice.getSchoolClasses(school_year_id, function(school_classes){
    		$scope.school_classes = school_classes.school_class_list;
            if ($scope.school_classes){
                $scope.school_classes_lenght = $scope.school_classes.length
            }
    	})
    }

    $scope.addSchoolSubject = function(school_subject){
        $scope.school_subject_obj = {}
        adminservice.addSchoolSubject(school_subject, function(school_subject_obj){
            $scope.school_subject_obj = school_subject_obj.school_subject_obj;
            $scope.getSchoolSubject()
            $scope.restart_form()

        })
    }


    $scope.uploadFile = function(user_id, image) {
            $scope.file = new FormData();
            $scope.file.append("file", image);
            $scope.upload_image(user_id)
        };


    $scope.upload_image= function(user_id) {
     $http.post(`${API_ENDPOINT.url}/upload/user/${user_id}`, $scope.file, {
           headers: {'Content-Type': undefined },
           transformRequest: angular.identity
          }).then(function(resp){
            $scope.user_obj.image = resp.data.image_obj
            $scope.restart_form()
        }, function(resp){
            console.log(resp.data)
        })}

    $scope.getSchoolSubject = function(){
        $scope.school_class_subject_view = 0
        $scope.user_list_lenght = 0
        $scope.school_subject_list = []
        adminservice.getSchoolSubject(function(school_subject_list){
            $scope.school_subject_list = school_subject_list.school_subject_list;
            if ($scope.school_subject_list) {
                $scope.school_subject_list_lenght = $scope.school_subject_list.length
            }
        })
    }

    $scope.show_class_details = function(school_class){
        $scope.user_list_lenght = 0
        $scope.school_class_details = school_class
        $scope.show_subtab = 1
    }

    $scope.add_more_students = function(){
        $scope.getUsers("Student")
        $scope.find_by_role("student")
        $scope.student_list = $scope.users
    }

    $scope.addnewClass = function(school_year_id, new_class){
        new_class.school_year_id = school_year_id
        adminservice.addClass(new_class, function(school_class_obj){
            $scope.school_class_obj = school_class_obj.school_class_obj
        })
        $scope.getSchoolClasses(school_year_id)
    }

    $scope.change_password = function(user_id, new_object){
        new_object.id = user_id
        adminservice.changePassword(new_object, function(){
        })
        $scope.restart_form()
    }

    $scope.add_students = function(class_id){
        adminservice.addStudentToClass(student_list_to_server, class_id, function(school_class_list){
            $scope.school_class_details.students = school_class_list.school_class_list
            /*for (var i = 0; i < $scope.users.length; i++ ) {
                for (var j = 0; j < $scope.school_class_details.students.length; j++ ) {
                    if ($scope.users[i].uniqueID == $scope.school_class_details.students[j].uniqueID) {
                        $scope.users[i].isDisabled = true
                        console.log($scope.users[i])
                    }
                    console.log('-----------------')
                }
            }*/
        })
        $scope.user_list_lenght = 0
    }   

    $scope.append_student = function($event, student_id){
        if ($event.target.checked){
            student_list_to_server.push(student_id)
        }
        else{
            student_list_to_server.splice(student_list_to_server.findIndex(element => element == student_id), 1)
        }
    }

    $scope.append_school_subject = function($event, school_subject_id){
        if ($event.target.checked){
            subject_list_to_server.push(school_subject_id)
        }
        else{
            subject_list_to_server.splice(subject_list_to_server.findIndex(element => element == school_subject_id), 1)
        }
    }

    $scope.add_subject = function(class_id){
        adminservice.addSubjectToClass(subject_list_to_server, class_id, function(school_class_list){
            $scope.school_class_subjects = school_class_list.school_class_list
        })
        $scope.user_list_lenght = 0
        $scope.school_class_subject_view = 0
    }

    $scope.getSchoolSubjectView = function(class_id){
        $scope.user_list_lenght = 0
        $scope.school_subject_list_lenght = 0
        adminservice.getSubjectFromClass(class_id, function(school_class_list){
            $scope.school_class_subjects = school_class_list.school_class_list
            if ($scope.school_class_subjects.length>0) {
                $scope.school_class_subject_view = 1
            }
        })
    }

    $scope.drop_subject = function(subject_id, class_id){
        adminservice.dropSubjectFromClass(subject_id, class_id, function(school_class_list){
            $scope.school_class_subjects = school_class_list.school_class_list
        })
    }


    $scope.drop_student = function(student_id, class_id){
        adminservice.dropStudentFromClass(student_id, class_id, function(school_class_list){
            $scope.get_class_students(class_id)
        })
    }

    $scope.get_class_students = function(class_id){
        adminservice.getStudentsFromClass(class_id, function(school_class_list){
            $scope.school_class_details.students = school_class_list.school_class_list
        })
    }


    $scope.add = function() {
    var f = document.getElementById('file').files[0],
        r = new FileReader();

    r.onloadend = function(e) {
      var data = e.target.result;
      console.log(data)
      $http(
    {
      url:'http://localhost:6543/upload',
      method: 'POST',
      data: data
    }).then(function(resp){
      console.log(resp)
    }, function(resp){
      console.log(resp)
    })
      //send your binary data via $http or $resource or do anything else with it
    }

    r.readAsBinaryString(f);
}




}])


.controller('professorController', ['$scope','$http','$q','$rootScope','adminservice','authservice', 'API_ENDPOINT', 'professorservice', function($scope, $http, $q, $rootScope, adminservice, auth, API_ENDPOINT, professorservice){
    $scope.show_tab = 0
    $scope.user_list_lenght = 0
    $scope.school_year_list_lenght = 0
    $scope.school_classes_lenght = 0
    $scope.school_subject_list_lenght = 0
    $scope.show_subtab = 0
    $scope.student_list = []
    $scope.userID = auth.user_id()
    let student_list_to_server = []
    let subject_list_to_server = []
    var temp_role = ''
    $scope.absencesShow = 0
    $scope.filteredTodos = []
    $scope.currentPage = 1
    $scope.maxSize = 5;
    $scope.class_list = []
    //$scope.totalItems = 0
    $scope.bigTotalItems = 175;
    $scope.bigCurrentPage = 1;
    $scope.totalItems = 0
    $scope.showMiss = 0
    $scope.picked_button = 0


    $scope.test_class = 'blue_button'


    $scope.set_grade = function(grade){
        $scope.grade = grade
        if (grade == 1) {
            $scope.picked_button = 1;
        };
        if (grade == 2) {
            $scope.picked_button = 2;
        };
        if (grade == 3) {
            $scope.picked_button = 3;
        };
        if (grade == 4) {
            $scope.picked_button = 4;
        };
        if (grade == 5) {
            $scope.picked_button = 5;
        };
        console.log($scope.grade)
    }

    $scope.add_new_grade = function(new_grade){
        console.log(new_grade)
        new_grade.grade = $scope.grade
        new_grade.student_id = $scope.student_class_details.student.id
        new_grade.subject_id = $scope.class_subject_id
        professorservice.addGrade($scope.school_class_id, new_grade, function(new_grade){
            $scope.grades.grades.push(new_grade.new_grade)
        })
    }


    $scope.forward_student_id = function(student_id){
        $scope.student_id = student_id
    }


    $scope.show_profile = function(){
        $scope.show_tab = 0
        $scope.disable_button = true
        var user_id = localStorage.getItem('user_id')
        $scope.getUser($scope.userID = user_id)
        $scope.show_tab = 1
        $scope.user_list_lenght = 0
        $scope.school_classes_lenght = 0
    }

    $scope.show_absences = function(class_id, date){
        console.log(class_id, date)
        professorservice.getAbsence(class_id, date, function(absence_list){
            $scope.absences = absence_list.absence_list
            console.log($scope.absences)
            if ($scope.absences.length > 0) {
                $scope.absencesShow = 1
            }
            else{
                $scope.absencesShow = 0
            }
        })
    }

    $scope.show_miss = function(){
        $scope.show_class_details = 0
        $scope.show_student_details = 0
        $scope.showMiss = 1
    }

    $scope.add_absence = function(class_id, absence_obj, student_id){
        absence_obj.student_id = student_id
        console.log(absence_obj)
        professorservice.addNewAbsence(class_id, absence_obj, function(absence){
        }
    )}

    $scope.show_add_absence_form = function(){
        $scope.absencesShow = 2
    }


    $scope.show_student = function(class_id, student_id){
        console.log($scope.userID)
        $scope.show_student_details = 1
        professorservice.getGrades(class_id, student_id, function(student_class_details){
            $scope.student_class_details = student_class_details.student_class_details
            console.log(student_class_details)
            console.log($scope.student_class_details.school_subjects)
        })
    }


    $scope.show_class = function(){
        $scope.show_class_details = 1
        $scope.showMiss = 0
    }


    $scope.numPages = function(){
        return $scope.class_list.school_class_student_list.length
    }

    $scope.join_class = function(school_class_id){
        $scope.school_class_id = school_class_id
        console.log($scope.school_class_id)
        adminservice.getClass(school_class_id, function(school_class_list){
            $scope.class_list = school_class_list
            if ($scope.class_list.school_class_student_list && $scope.class_list.school_class_subject_list) {
                $scope.show_subtab = 1
                $scope.totalItems = $scope.class_list.school_class_student_list.length
            }
            console.log($scope.class_list)
        })
    }

    $scope.show_student_grade = function(grades){
        $scope.grades = grades
        $scope.class_subject_id = grades.id
    }


    $scope.show_users = function(){
        $scope.show_tab = 0
        $scope.users = [];
        $scope.user_list_lenght = 0
        // Može se koristiti
        //$scope.user_list_lenght = 0
        $scope.getRoles()
        $scope.show_tab = 2
        $scope.school_classes_lenght = 0
    }

    $scope.find_by_role = function(role){
        $scope.school_subject_list_lenght = 0
        $scope.school_class_subject_view = 0
        temp_role = role
        $scope.getUsers(role)
    }

    $scope.show_classes = function(){
        $scope.show_tab = 0
        $scope.show_subtab = 0
        $scope.user_list_lenght = 0
        $scope.find_by_role("Professor")
        $scope.get_school_years()
        $scope.show_tab = 3
    }
    
    $scope.show_subjects = function(){
        $scope.show_tab = 0
        $scope.find_by_role("Professor")
        $scope.getSchoolSubject()
        $scope.show_tab = 4
    }


    $scope.lista = []
    for (var i = 0; i<50; i++) {
        $scope.lista.push(i)
    }

    $scope.getUsers = function(role){
        $scope.users = [];
        adminservice.getUsers(role,function(users){
            $scope.users = users;
            if($scope.users){
            $scope.user_list_lenght = $scope.users.length
        }
        });
      }

    $scope.addSchoolSucject = function(new_subject){
    }

    $scope.getRoles = function(){
        $scope.roles = [];
        adminservice.getRoles(function(roles){
            $scope.roles = roles;
        });
      }

    $scope.getUser = function(user_id){
        $scope.user_obj = {}
        adminservice.getUser(user_id, function(user_obj){
            $scope.user_obj = user_obj;
            $scope.user_obj.edit_birth_date = new Date($scope.user_obj.birth_date)
        })
    }

    $scope.change_tab = function(user_id){
        $scope.show_tab = 0
        $scope.disable_button = false
        $scope.getUser(user_id)
        $scope.show_tab = 1
    }

    $scope.addUser = function(user){
        var date = new Date(user.birth_date)
        date = date.setDate(date.getDate() + 1)
        user.birth_date = new Date(date)
        $scope.user_obj = {}
        adminservice.addUser(user, function(user_obj){
            $scope.user_obj = user_obj;
        })
    }

    $scope.editUser = function(user){
        var date = new Date(user.edit_birth_date)
        date = date.setDate(date.getDate())
        user.birth_date = new Date(date)
        console.log(user.birth_date)
        adminservice.editUser(user, function(user_obj){
            $scope.user_obj = user_obj.user_obj;
            $scope.user_obj.edit_birth_date = new Date(user_obj.user_obj.birth_date)
        })
    }

    $scope.restart_form = function(){
        $scope.new_user = {}
        $scope.new_subject = {}
        $scope.file = {}
        $scope.files = {}
        $scope.image = {}
        $scope.myFile = ""
        $scope.new_class = {}
        $scope.new_obj = {}
        $scope.new_object = {}
        $scope.user_list_lenght = 0
        $scope.school_subject_list_lenght = 0
        $scope.school_class_subject_view = 0
        var image_id = document.getElementById("inputImage")
        image_id.value = ''
        $scope.absencesShow = 0
        $scope.showMiss = 0
    }

    $scope.activate_user = function(user_id){
        adminservice.activateUser(user_id, function(user_obj){
            $scope.user_obj.activated = user_obj.activated;
        })
        $scope.getUsers(temp_role)
    }

    $scope.deactivate_user = function(user_id){
        adminservice.deactivateUser(user_id, function(user_obj){
            $scope.user_obj.activated = user_obj.user_deactivated;
        })
        $scope.getUsers(temp_role)
    }

    $scope.delete_user = function(user_id){
        $scope.show_tab = 0
        adminservice.deleteUser(user_id, function(user_obj){
        })
        $scope.getUsers(temp_role)
    }

    $scope.get_school_years = function(){
        $scope.school_years = []
        adminservice.getSchoolYears(function(school_years){
            $scope.school_years = school_years.school_year_list;
            if ($scope.school_years) {
                $scope.school_year_list_lenght = $scope.school_years.length
            }
        })
    }

    $scope.addSchoolYear = function(school_year){
        $scope.school_year_obj = {}
        adminservice.addSchoolYears(school_year, function(school_year_obj){
            $scope.school_year_obj = school_year_obj;
            $scope.get_school_years()
        })
    }

    $scope.find_by_school_year_id = function(school_year_id){
        $scope.getSchoolClasses(school_year_id)
    }
    
    $scope.getSchoolClasses = function(school_year_id){
        $scope.school_classes = []
        adminservice.getSchoolClasses(school_year_id, function(school_classes){
            $scope.school_classes = school_classes.school_class_list;
            if ($scope.school_classes){
                $scope.school_classes_lenght = $scope.school_classes.length
            }
        })
    }

    $scope.addSchoolSubject = function(school_subject){
        $scope.school_subject_obj = {}
        adminservice.addSchoolSubject(school_subject, function(school_subject_obj){
            $scope.school_subject_obj = school_subject_obj.school_subject_obj;
            $scope.getSchoolSubject()
            $scope.restart_form()

        })
    }


    $scope.uploadFile = function(user_id, image) {
            $scope.file = new FormData();
            $scope.file.append("file", image);
            $scope.upload_image(user_id)
        };


    $scope.upload_image= function(user_id) {
     $http.post(`${API_ENDPOINT.url}/upload/user/${user_id}`, $scope.file, {
           headers: {'Content-Type': undefined },
           transformRequest: angular.identity
          }).then(function(resp){
            $scope.user_obj.image = resp.data.image_obj
            $scope.restart_form()
        }, function(resp){
            console.log(resp.data)
        })}

    $scope.getSchoolSubject = function(){
        $scope.school_class_subject_view = 0
        $scope.user_list_lenght = 0
        $scope.school_subject_list = []
        adminservice.getSchoolSubject(function(school_subject_list){
            $scope.school_subject_list = school_subject_list.school_subject_list;
            if ($scope.school_subject_list) {
                $scope.school_subject_list_lenght = $scope.school_subject_list.length
            }
        })
    }

    $scope.show_class_details = function(school_class){
        $scope.user_list_lenght = 0
        $scope.school_class_details = school_class
        $scope.show_subtab = 1
    }

    $scope.add_more_students = function(){
        $scope.getUsers("Student")
        $scope.find_by_role("student")
        $scope.student_list = $scope.users
    }

    $scope.addnewClass = function(school_year_id, new_class){
        new_class.school_year_id = school_year_id
        adminservice.addClass(new_class, function(school_class_obj){
            $scope.school_class_obj = school_class_obj.school_class_obj
        })
        $scope.getSchoolClasses(school_year_id)
    }

    $scope.change_password = function(user_id, new_object){
        new_object.id = user_id
        adminservice.changePassword(new_object, function(){
        })
        $scope.restart_form()
    }

    $scope.add_students = function(class_id){
        adminservice.addStudentToClass(student_list_to_server, class_id, function(school_class_list){
            $scope.school_class_details.students = school_class_list.school_class_list
            /*for (var i = 0; i < $scope.users.length; i++ ) {
                for (var j = 0; j < $scope.school_class_details.students.length; j++ ) {
                    if ($scope.users[i].uniqueID == $scope.school_class_details.students[j].uniqueID) {
                        $scope.users[i].isDisabled = true
                        console.log($scope.users[i])
                    }
                    console.log('-----------------')
                }
            }*/
        })
        $scope.user_list_lenght = 0
    }   

    $scope.append_student = function($event, student_id){
        if ($event.target.checked){
            student_list_to_server.push(student_id)
        }
        else{
            student_list_to_server.splice(student_list_to_server.findIndex(element => element == student_id), 1)
        }
    }

    $scope.append_school_subject = function($event, school_subject_id){
        if ($event.target.checked){
            subject_list_to_server.push(school_subject_id)
        }
        else{
            subject_list_to_server.splice(subject_list_to_server.findIndex(element => element == school_subject_id), 1)
        }
    }

    $scope.add_subject = function(class_id){
        adminservice.addSubjectToClass(subject_list_to_server, class_id, function(school_class_list){
            $scope.school_class_subjects = school_class_list.school_class_list
        })
        $scope.user_list_lenght = 0
        $scope.school_class_subject_view = 0
    }

    $scope.getSchoolSubjectView = function(class_id){
        $scope.user_list_lenght = 0
        $scope.school_subject_list_lenght = 0
        adminservice.getSubjectFromClass(class_id, function(school_class_list){
            $scope.school_class_subjects = school_class_list.school_class_list
            if ($scope.school_class_subjects.length>0) {
                $scope.school_class_subject_view = 1
            }
        })
    }

    $scope.drop_subject = function(subject_id, class_id){
        adminservice.dropSubjectFromClass(subject_id, class_id, function(school_class_list){
            $scope.school_class_subjects = school_class_list.school_class_list
        })
    }


    $scope.drop_student = function(student_id, class_id){
        adminservice.dropStudentFromClass(student_id, class_id, function(school_class_list){
            $scope.get_class_students(class_id)
        })
    }

    $scope.get_class_students = function(class_id){
        adminservice.getStudentsFromClass(class_id, function(school_class_list){
            $scope.school_class_details.students = school_class_list.school_class_list
        })
    }

    $scope.get_class = function(class_id){
        console.log('Work')
        adminservice.getClass(class_id, function(school_class_list){
            $scope.class_list = school_class_list
            console.log($scope.class_list)
        })
    }

    $scope.add = function() {
    var f = document.getElementById('file').files[0],
        r = new FileReader();

    r.onloadend = function(e) {
      var data = e.target.result;
      console.log(data)
      $http(
    {
      url:'http://localhost:6543/upload',
      method: 'POST',
      data: data
    }).then(function(resp){
      console.log(resp)
    }, function(resp){
      console.log(resp)
    })
      //send your binary data via $http or $resource or do anything else with it
    }

    r.readAsBinaryString(f);
}




}])


.run(function($transitions,$state,authservice){
    
    $transitions.onStart({ to:'*'},function(){
      
      if(!authservice.isAuthenticated()){
        $state.go('login');
      }
     });
    
    
  })
