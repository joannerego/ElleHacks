
var x;

function myFunction() {
  x = document.getElementById("myURL").value;

  read();
}

const input = new File(1, "database.txt");
var reader = new FileReader();
reader.onload = function(evt) {
  console.log(evt.target.result);
};
reader.readAsText(input);
