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

    // ✅ Move word wheel logic here
    const form = document.getElementById("word-wheel-form");
    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const centre = document.getElementById("centre-letter").value.trim().toLowerCase();
            const outer = document.getElementById("outer-letters").value.trim().toLowerCase().split("");
            
            try {
                const res = await fetch("/api/solve", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ centre_letter: centre, outer_letters: outer }),
                });

                const data = await res.json();
                const resultsDiv = document.getElementById("word-wheel-results");

                if (data.words.length === 0) {
                    resultsDiv.textContent = "No words found.";
                } else {
                    resultsDiv.innerHTML = "<ul>" + data.words.map(w => `<li>${w}</li>`).join("") + "</ul>";
                }
            } catch (error) {
                console.error("Error calling solve API:", error);
            }
        });
    }
});