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
		.state('test',{url:'/test', templateUrl:'new_user.html'})
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


.controller('adminController', ['$scope','$http','$q', function($scope,$http,$q){
	$scope.show_tab = 0
	$scope.user_list_lenght = 0


	$scope.show_profile = function(){
		$scope.show_tab = 0
		$scope.show_tab = 1
		$scope.user_list_lenght = 0
		console.log($scope.show_tab)
	}

	$scope.show_users = function(){
		$scope.show_tab = 0
		roles(function(resp){
			$scope.roles = resp
		})
		//console.log($scope.users)
		$scope.show_tab = 2
	}

	$scope.find_by_role = function(role){
		console.log(role)
		users(role,function(resp){
			$scope.users = resp
			console.log(resp)
		})
	}

	$scope.show_classes = function(){
		$scope.show_tab = 0
		$scope.show_tab = 3
		$scope.user_list_lenght = 0
		console.log($scope.show_tab)
	}
	//console.log($state.params)
	$scope.lista = []
	for (var i = 0; i<50; i++) {
		$scope.lista.push(i)
	}

	function users(role, callback){
          $http({
            url: 'http://localhost:6543/users/'+role,
            method: 'GET',
            data: role
          }).then(function(resp){
          	callback(resp.data.user_list)
          	$scope.user_list_lenght = resp.data.user_list.length
          }, function(resp){
            console.log(resp)
          })
        }
        
    function roles(callback){
    	$http({
    		url:'http://localhost:6543/roles',
    		method: 'GET'
    	}).then(function(resp){
    		callback(resp.data.role_list)
    		console.log(resp.data.role_list.length)
    	}), function(resp){

    	}
    }


}])


.run(function($transitions,$state,authservice){
    
    $transitions.onStart({ to:'*'},function(){
      
      if(!authservice.isAuthenticated()){
        $state.go('login');
      }
     });
    
    
  })
