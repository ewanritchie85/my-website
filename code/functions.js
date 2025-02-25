$(document).ready(function(){
    // This function creates a quick fade in when moving between web pages
    $("body").css("display", "none");
    $("body").fadeIn(300);

    // Creates a double fade out/fade in on the image
    $("#mug-shot").click(function(){
        $("#mug-shot").fadeOut("300");
        $("#mug-shot").fadeIn("300");
        $("#mug-shot").fadeOut("300");
        $("#mug-shot").fadeIn("300");
      });


    //   if answer to quiz is false, paragraph is revealed and quiz is hidden
    //   if true, a failure message is revealed
    $("#quiz").submit(function(event){
        event.preventDefault();
        var answer = $('input[name="answer"]:checked').val();
        if(answer=="false"){
        $("#blurb").css("color","rgb(202, 202, 202)");
        $("#blurb-link").css("color","rgb(67, 111, 255)");
        $("#paragraph").fadeIn("200");
        $("#wrong").hide();
        } else {
            $("#wrong").css("color","rgb(202, 202, 202)");
        }
        $("#quiz").hide("slow");
        $("#quiz-title").hide("slow");
    })


});


