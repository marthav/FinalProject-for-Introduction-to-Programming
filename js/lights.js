/* This defines a function which turns off every light by removing the "on" class from the HTML elements.
 */
var TERMS = document.getElementsByClassName("term");

function allOff() {
  for (var i=0; i<TERMS.length; i = i+1) {
    TERMS[i].classList.remove("on");
  }
} // <= CRITICAL: you MUST close this function here

var allOn= function() {
  for (var i=0; i<TERMS.length; i = i+1) {
    TERMS[i].classList.add("on");
  }
}

  function switchTerm(target_class) {
    allOff();
  // } CRITICAL: this bracket is disrupting function definition...MUST remove

  var target_nodes = document.getElementsByClassName(target_class);
  
 // for (var j=0; j < target_class.length; j++)  { // <= target_class is a String...not what you want
  for (var j=0; j < target_nodes.length; j++)  {  // <= target_nodes is what you want to loop over
    target_nodes[j].classList.add("on"); // <= this has to be target_nodes, the List
  }
}



