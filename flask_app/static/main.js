$(document).ready(function () {

    $("#update-database").click(function () {
        $(".progress-bar").css("display", "block")
    });

    $("#filter-reset").click(clearFilters)
});

setGridRows = function () {
    var elem = document.getElementsByClassName
}

progressBarAnimation = function () {
    var elem = document.getElementById("myBar");
    var width = 0;
    var id = setInterval(frame, 10);

    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
}

clearFilters = function () {
    selectTags = document.getElementsByTagName("select");

    for (var i = 0; i < selectTags.length; i++) {
        selectTags[i].selectedIndex = 0;
    }
}
