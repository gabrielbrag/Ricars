document.addEventListener("DOMContentLoaded", function () {
    if (window.innerWidth >= 992) { // 992 pixels is the breakpoint for large screens (lg)
        var sidebar = document.getElementById("sidebar");
        sidebar.classList.remove("collapse")
    }
});