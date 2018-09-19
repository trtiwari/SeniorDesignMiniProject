function onSignIn(googleUser) {
	// this is the Google Sign in call back function that is invoked as soon as a 
	// user signs in
  var profile = googleUser.getBasicProfile();
  var id = profile.getId();
  var name =  profile.getName();
  window.location.href = id +"/list_sources";
}