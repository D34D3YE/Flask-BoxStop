function deleteNote(noteId) {
  fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId })
  }).then((_res) => {
      window.location.href ="/notes";
  });
}

function deleteAusgabe(ausgabeId){
  fetch("/delete-ausgabe", {
      method: "POST",
      body: JSON.stringify({ ausgabeId: ausgabeId })
  }).then((_res) => {
      window.location.href = "/ausgaben";
  });
}

function deleteFahrt(fahrtId){
  fetch("/delete-fahrt", {
      method: "POST",
      body: JSON.stringify({fahrtId: fahrtId })
  }).then((_res) => {
      window.location.href = "/fahrtenbuch";
  });
}

function toggleErweiterteInformationen(event) {
  var kachel = event.target;
  var erweiterteInformationen = kachel.querySelector('.erweiterte-informationen');
  
  if (erweiterteInformationen.style.display === 'block') {
    erweiterteInformationen.style.display = 'none';
  } 
  else {
    erweiterteInformationen.style.display = 'block';
  }
}

function openGoogleMaps(address) {
  var url = "https://www.google.com/maps/dir/?api=1&destination=" + encodeURIComponent(address);
  window.open(url);
}

function validateForm() {
  var startKm = parseInt(document.forms["myForm"]["street_start_km_form"].value);
  var endKm = parseInt(document.forms["myForm"]["street_end_km_form"].value);
  
  if (endKm < startKm) {
    alert("Der Kilometerstand beim Ende darf nicht kleiner sein als beim Anfang.");
    return false;
  }
  return true;
}