function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  var id = profile.getId(); // Do not send to your backend! Use an ID token instead.
  var name =  profile.getName();
  document.location.replace("http://trishita.ddns.net/" + name + "/" + id +"/add_sources");
}