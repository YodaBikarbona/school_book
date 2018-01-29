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




.controller('loginController', ['$scope','authservice','$rootScope','$state','ROLE', function($scope,auth,$rootScope,$state,ROLE){

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

.controller('mainController', ['$scope','$rootScope','authservice',function($scope,$rootScope,auth){
    $scope.logout = function(){
      auth.logout();
    }
}])


.controller('adminController', ['$scope','$state', function($scope, $state){
	$scope.show_tab = 0


	$scope.show_profile = function(){
		$scope.show_tab = 0
		$scope.show_tab = 1
		console.log($scope.show_tab)
	}

	$scope.show_users = function(){
		$scope.show_tab = 0
		$scope.show_tab = 2
		console.log($scope.show_tab)
	}

	$scope.show_classes = function(){
		$scope.show_tab = 0
		$scope.show_tab = 3
		console.log($scope.show_tab)
	}
	//console.log($state.params)
	
}])
