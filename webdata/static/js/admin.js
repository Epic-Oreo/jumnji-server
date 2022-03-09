function command(commandName){

  let form = document.getElementById("hidden-command-form");
  let commandZone = document.getElementById("hidden-command");

  
  if (commandName == "addCard") {
    let person = prompt("Name of recipient of card");
    let card = prompt("Id of card");
    commandZone.value = "addCard:"+card+":"+person;
  }
  else if (commandName == "checkAdmin") {
    let person = prompt("Name of person");
    commandZone.value = "checkAdm in:"+person;
  }
  form.submit();
}

function replaceHref(){

  let acb = document.getElementById("allCardsButton");

  acb.href = "allCards/"+localStorage.getItem('token')
}