angular.module('school_book', ['ui.router'])

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


.controller('adminController', ['$scope','$http','$q','$rootScope','adminservice','authservice', function($scope,$http,$q,$rootScope,adminservice,auth){
	$scope.show_tab = 0
	$scope.user_list_lenght = 0
	$scope.school_year_list_lenght = 0
	$scope.userID = auth.user_id()
	var temp_role = ''


	$scope.show_profile = function(){
		$scope.show_tab = 0
		$scope.disable_button = true
		//var user_id = localStorage.getItem('user_id')
		//var user_id = auth.user_id()
		$scope.getUser($scope.userID = auth.user_id())
		//console.log(user_id)
		$scope.show_tab = 1
		$scope.user_list_lenght = 0
	}

	$scope.show_users = function(){
		$scope.show_tab = 0
		// Može se koristiti
		//$scope.user_list_lenght = 0
		$scope.getRoles()
		$scope.show_tab = 2
	}

	$scope.find_by_role = function(role){
		temp_role = role
		$scope.getUsers(role)
	}

	$scope.show_classes = function(){
		$scope.show_tab = 0
		$scope.get_school_years()
		$scope.show_tab = 3
		$scope.user_list_lenght = 0
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
    		console.log(user_obj)
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

    $scope.restart_form = function(){
    	$scope.new_user = {}
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
    		console.log($scope.school_years)
    	})
    }

    $scope.get_school_years = function(){
    	$scope.school_years = []
    	adminservice.getSchoolYears(function(school_years){
    		$scope.school_years = school_years.school_year_list;
    		if ($scope.school_years) {
    			$scope.school_year_list_lenght = $scope.school_years.length
    		}
    		console.log($scope.school_years)
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
    	console.log(school_year_id)
    	$scope.getSchoolClasses(school_year_id)
    }
    
    $scope.getSchoolClasses = function(school_year_id){
    	$scope.school_classes = []
    	adminservice.getSchoolClasses(school_year_id, function(school_classes){
    		$scope.school_classes = school_classes;
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
