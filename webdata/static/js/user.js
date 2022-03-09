function utf8_to_b64( str ) {
  return window.btoa(unescape(encodeURIComponent( str )));
}

function b64_to_utf8( str ) {
  return decodeURIComponent(escape(window.atob( str )));
}



function check_for_login(){

  const localtoken = b64_to_utf8(localStorage.getItem('token'));

  if (localtoken) {
    console.log("Auto login")


    let loginForm = document.getElementById('hidden-form');
    let tokenField = document.getElementById('token-field');

    tokenField.value = localtoken;

    loginForm.submit();


    // .submit();
  }
}

function logout() {
  localStorage.removeItem('token');
  window.location.href = "/";
}


function resLogout() {
  if (window.confirm("Do you really want to reset")) {
    logout();
  }
}