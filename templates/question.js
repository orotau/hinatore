<script>
  console.log("some random text for testing");
  document.onkeypress = key_pressed;

  var myVar;

  function myFunction() {
    document.getElementById("nw").focus();
    console.log(document.activeElement.id);
    myVar = setInterval(alertFunc, 3000);
  }

  function alertFunc() {
    switch (document.activeElement.id) {
      case "nw":
      document.getElementById("ne").focus();
      break;
      case "ne":
      document.getElementById("se").focus();
      break;
      case "se":
      document.getElementById("sw").focus();
      break;
      case "sw":
      document.getElementById("nw").focus();
      break;
    }
  }

  function key_pressed(event) {
    /*

    */
    if (event.key === "1") {
      alert(document.activeElement.id);
      clearInterval(myVar);
      var newURL;
      newURL = window.location.href + "answer/" + document.activeElement.id;
      window.location.assign(newURL);
    }
    }
</script>
