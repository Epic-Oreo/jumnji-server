function b64_to_utf8( str ) {
  return decodeURIComponent(escape(window.atob( str )));
}



function redirectGet(){
  // token-input
  let token = b64_to_utf8(localStorage.getItem('token'));
  let form = document.getElementById("hidden-form");
  let tokenform = document.getElementById("token-input");

  tokenform.value = token

  form.submit()

}