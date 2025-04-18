$(document).ready(function() {
    //a quick fade in when moving between pages
    $(".page-content").css("display", "none");
    $(".page-content").fadeIn(1000);

    $("#mug-shot").click(function(){
        $("#mug-shot").fadeOut("300");
        $("#mug-shot").fadeIn("300");
    });

    $(".experience").hide();
    $("#ten10").show(); // Default visible experience

    // Handle clicking on the list items
    $(".experience-list li").click(function() {
        // Remove active class from all experiences
        $(".experience").removeClass('active').hide();

        // Show the selected experience
        var experienceId = $(this).data('experience');
        $("#" + experienceId).addClass('active').fadeIn();
    });

});