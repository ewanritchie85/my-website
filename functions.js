$(document).ready(function () {
    $(".page-content").css("display", "none").fadeIn(300);

    $("#mug-shot").click(function () {
        $("#mug-shot").fadeOut(300).fadeIn(300);
    });

    $(".experience").hide();

    const firstExperienceId = $(".experience-list li").first().data("experience");
    $("#" + firstExperienceId).show().addClass("active");
    $(".experience-list li").first().addClass("active");

    $(".experience-list li").click(function () {
        $(".experience").removeClass("active").hide();

        const experienceId = $(this).data("experience");
        $("#" + experienceId).fadeIn().addClass("active");

        $(".experience-list li").removeClass("active");
        $(this).addClass("active");
    });

    $('.certs-row img').on('click', function () {
        $('#lightbox-img').attr('src', $(this).attr('src'));
        $('#lightbox-modal').css('display', 'flex').hide().fadeIn(300);
    });

    $('#lightbox-modal, #lightbox-img').on('click', function (e) {
        $('#lightbox-modal').fadeOut(300);

    });

});