
/* This defines a function which turns off every light by removing the "on" class from the HTML elements.*/

var TERMS = document.getElementsByClassName("term");

function allOff() {
  for (var i=0; i<TERMS.length; i = i+1) {
    TERMS[i].classList.remove("on");
  }


// switch term has been called! 
function switchTerm(target_class) {
   console.log(target_class); // what was passed in...?
// in this situation target_class is equal to "program"
allOff();
}
  // at this time lets create a list/array containing ONLY the target elements we want to "turn on"
  var target_nodes = document.getElementsByClassName(target_class);// need a way to search HTML page for all elements with className "program"

  // use a for loop to iterate over that sub-list
  // review this link for how to loop over node list...see EXAMPLE section
  // https://developer.mozilla.org/en-US/docs/Web/API/NodeList
 //for ( ...set up the for loop... ) { 
   //   target_node[i].classList.add("on"); // "turn on" each of those nodes!
  for (var j=0; j < target_class.length; j ++)  { 
  target_class[j].classList.add("on"); // "turn on" each of those nodes!
  }
}



