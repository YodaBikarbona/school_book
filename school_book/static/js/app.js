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

.controller('loginController', ['$scope','$state', function($scope, $state){

	$scope.login = (user) => {
		if(user.username == 'mihael.peric@hotmail.com'){
			$state.go('admin', {user:{
				username: user.username
				password: '12345'
			}})
		}
	}
	
}])

.controller('adminController', ['$scope','$state', function($scope, $state){

	console.log($state.params)
	
}])
