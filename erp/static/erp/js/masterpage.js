document.addEventListener("DOMContentLoaded", function () {
    console.log("toogler")

    if (window.innerWidth >= 728) { // 992 pixels is the breakpoint for large screens (lg)
        var sidebar = document.getElementById("sidebar");
        sidebar.classList.remove("collapse")
    }
});