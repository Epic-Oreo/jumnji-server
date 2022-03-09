function utf8_to_b64( str ) {
  return window.btoa(unescape(encodeURIComponent( str )));
}

function b64_to_utf8( str ) {
  return decodeURIComponent(escape(window.atob( str )));
}



function setLogin(token) {
  localStorage.setItem("token", utf8_to_b64(token));
  // console.log("setting")

}

function goToPage(pageURL){
  // hidden-misc-form
  let form = document.getElementById("hidden-misc-form")

  form.action = pageURL

  form.submit()

}


if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}


var i = 0;
function progress(end) {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("progressBar");
    var width = 10;
    var id = setInterval(frame, 1);
    function frame() {
      if (width >= end) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
        elem.innerHTML = width  + "%";
      }
    }
  }
}