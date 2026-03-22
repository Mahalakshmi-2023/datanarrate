// Highlight the active nav link based on current URL
$(document).ready(function () {
  const path = window.location.pathname;
  $(".nav-link").each(function () {
    if ($(this).attr("href") === path) {
      $(this).addClass("active text-warning");
    }
  });
});
