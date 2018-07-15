<script>
  document.onkeypress = key_pressed;

  function key_pressed(event) {
    /*

    */
      if (event.key === "1") {
        var pathArray = window.location.pathname.split( '/' );
        var selection = pathArray[pathArray.length - 1];
        var questions_total = pathArray[pathArray.length - 2];
        var question_number = pathArray[pathArray.length - 3];
        var question_group = pathArray[pathArray.length - 4];
        var newURL;
        if (question_number === questions_total) {
          // we are done - go to final page
          newURL = window.location.protocol + "//" +
                   window.location.host + "/" +
                   question_group + "/" +
                   question_number + "/" +
                   questions_total + "/" +
                   "hinatore";
        }
        else {
          // go to next question
          next_question_number = parseInt(question_number, 10) + 1
          newURL = window.location.protocol + "//" +
                   window.location.host + "/" +
                   question_group + "/" +
                   next_question_number + "/" +
                   questions_total;
        }
        window.location.assign(newURL);
       }
    }
</script>
