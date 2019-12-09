$(document).ready(() => {

    $("#update-database").click(() => {
        $(".progress-bar").css("display", "block")
    });

    // Updates city list based on selected county
    function dynamicCityList () {
        $("#county").on("change", function () {
            const county = $(this).val();
    
            console.log(county);
            console.log($("#city").val())
    
            $.ajax({
                method: "GET",
                url: "static/NJParcels_CityNums.json"
            }).then(json => {
                const cities = Object.keys(json[county]);
                $("#city").empty();
                cities.forEach(city => {
                    const opt = $("<option>").text(city).val(city);
                    $("#city").append(opt);
                });
                $("#city").prepend($("<option>").text("--All--").val("--All--"));
            });
        });
    };

    $("#filter-reset").click(clearFilters);

    // dynamicTableID();

    // setGridRows = function () {
    //     var elem = document.getElementsByClassName
    // }

    function progressBarAnimation () {
        const elem = document.getElementById("myBar");
        let width = 0;
        let id = setInterval(frame, 10);

        function frame() {
            if (width >= 100) {
                clearInterval(id);
            } else {
                width++;
                elem.style.width = width + '%';
            };
        };
    };

    function clearFilters () {
        const selectTags = document.getElementsByTagName("select");

        selectTags.forEach(tag => {
            tag.selectedIndex = 0;
        });
    };

    function sortByHeader () {
        const headers = document.getElementsByClass("grid-header");

        header.forEach(element => {
            element.addEventListener
        });

        // headerTag.setAttribute("sort_by", "city_asc")
    };

    function dynamicTableID () {
        element = document.getElementById("data-table-body");
        table_rows = element.children;

        for (let i = 0; i < table_rows.length; i++) {
            table_rows[i].id = `row_${i}`;
        };
    };

});