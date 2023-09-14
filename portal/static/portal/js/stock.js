document.addEventListener("DOMContentLoaded", function () {
    // Check the screen width and disable collapse on desktop

    if (window.innerWidth >= 992) { // 992 pixels is the breakpoint for large screens (lg)
        var filterToggle = document.getElementById("collapse-control");

        if (filterToggle.hasAttribute("data-toggle")) {
            filterToggle.removeAttribute("data-toggle");
        }
    }
});