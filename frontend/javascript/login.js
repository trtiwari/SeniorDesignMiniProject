function onSignIn(googleUser) {
	// this is the Google Sign in call back function that is invoked as soon as a 
	// user signs in

	window.onbeforeunload = function load_func(argument) {
		gapi.auth2.getAuthInstance().signOut();
	}
	var profile = googleUser.getBasicProfile();
	var id_token = googleUser.getAuthResponse().id_token;
	var id = profile.getId();
	var name =  profile.getName();

	var auth2 = gapi.auth2.getAuthInstance();
	auth2.disconnect();

	window.location.href = id +"/list_sources";
}