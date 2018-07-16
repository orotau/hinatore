<script>
  console.log("some random text for testing");
  document.onkeypress = key_pressed;

  var interval_timer;

  function startMovingFocus() {
    document.getElementById("nw").focus();
    interval_timer = setInterval(moveFocus, 1000*{{dwell_time.dwell_time|int}});
  }

  function moveFocus() {
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
      clearInterval(interval_timer);
      var newURL;
      var selection = document.activeElement.id;
      var db_column
      switch(selection) {
        case "nw":
            db_column = "{{ui_data.nw[1]}}";
            break;
        case "ne":
            db_column = "{{ui_data.ne[1]}}";
            break;
        case "se":
            db_column = "{{ui_data.se[1]}}";
            break;
        case "sw":
            db_column = "{{ui_data.sw[1]}}";
            break;
      }
      newURL = window.location.href + "/" +
               selection +
               "?db_column=" +
               db_column;
      window.location.assign(newURL);
    }
    }
</script>
