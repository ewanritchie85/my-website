$(document).ready(function () {
    // Fade in the page content
    $(".page-content").css("display", "none").fadeIn(1000);

    // Mug shot flicker effect
    $("#mug-shot").click(function () {
        $("#mug-shot").fadeOut(300).fadeIn(300);
    });

    // Hide all experiences
    $(".experience").hide();

    // Show the first listed experience by default
    const firstExperienceId = $(".experience-list li").first().data("experience");
    $("#" + firstExperienceId).show().addClass("active");
    $(".experience-list li").first().addClass("active");

    // Handle clicking on the experience list items
    $(".experience-list li").click(function () {
        $(".experience").removeClass("active").hide();

        const experienceId = $(this).data("experience");
        $("#" + experienceId).fadeIn().addClass("active");

        $(".experience-list li").removeClass("active");
        $(this).addClass("active");
    });
});