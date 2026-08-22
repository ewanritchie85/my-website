// Injects navbar.html into the #site-navbar div
fetch('navbar.html')
  .then(response => response.text())
  .then(html => {
    document.getElementById('site-navbar').innerHTML = html;
    // Re-initialize jQuery handlers for dynamically loaded content
    if (window.jQuery) {
      $(function() {
        if ($('#mug-shot').length) {
          $('#mug-shot').off('click').on('click', function () {
            $('#mug-shot').fadeOut(300).fadeIn(300);
          });
        }
      });
    }
  });
