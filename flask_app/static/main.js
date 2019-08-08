// function move() {
//     var elem = document.getElementById("myBar");
//     var width = 1;
//     var id = setInterval(frame, 10);

//     function frame() {
//         if (width >= 100) {
//             clearInterval(id);
//         } else {
//             width++;
//             elem.style.width = width + '%';
//         }
//     }
// }

clearFilters = function () {
    selectTags = document.getElementsByTagName("select");

    for (var i = 0; i < selectTags.length; i++) {
        selectTags[i].selectedIndex = 0;
    }
}

$(document).ready(function () {
    $("#update-database").click(function () {
        $.ajax({
            method: "POST",
            url: "/update_database",
            async: "asynchronous",
            success: function () {
                console.log("Database Update - SUCCESS")
            },
            error: function (request, status, error) {
                console.log("Error: " + error)
            }
        })
    });

    $("#update-database").click(function () {
        $(".progress-bar-container").css("display", "block")
    });

    $("#filter-clear").click(clearFilters)
});