
/* This defines a function which turns off every light by removing the "on" class from the HTML elements.*/

var TERMS = document.getElementsByClassName("term");

function allOff() {
  for (var i=0; i<TERMS.length; i = i+1) {
    TERMS[i].classList.remove("on");
  }
}

/* This defines a function which first turns off every light and then immediately turns one on.*/
function switchTerm(termNumber) {
  allOff();
  var term = TERMS[termNumber];
  term.classList.add("on");
}