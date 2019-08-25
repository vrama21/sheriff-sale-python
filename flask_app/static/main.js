$(document).ready(function () {

    $("#update-database").click(function () {
        $(".progress-bar").css("display", "block")
    });

    $("#filter-reset").click(clearFilters)

    dynamicTableID();

});

setGridRows = function () {
    var elem = document.getElementsByClassName
}

const progressBarAnimation = function () {
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

const clearFilters = function () {
    selectTags = document.getElementsByTagName("select");

    for (var i = 0; i < selectTags.length; i++) {
        selectTags[i].selectedIndex = 0;
    }
}

const sortByHeader = function () {
    headers = document.getElementsByClass("grid-header")

    for (var i= 0; i < headers.length; i++) {
        headers[i].addEventListener
    }

    // headerTag.setAttribute("sort_by", "city_asc")
}

const dynamicTableID = function () {
    element = document.getElementById("data-table-body")
    table_rows = element.children

    for (let i = 0; i < table_rows.length; i++) {
        table_rows[i].id = "row_" + i
    }
}