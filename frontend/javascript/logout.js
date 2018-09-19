  function signOut() {
    // Google sign out callback function invoked when the user signs out
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
      window.location.href = "/"
    });
  }
  
 function onLoad() {
    // loading Google Sign in dependencies
      gapi.load('auth2', function() {
        gapi.auth2.init();
      });
    }
