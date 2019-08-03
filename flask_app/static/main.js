function move() {
    var elem = document.getElementById("myBar");
    var width = 1;
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

// TODO: Requires AJAX -- Need to understand further
function UpdateDatabase() {
    const submit = document.getElementById("updateDatabase");
    const updateFunction = $.ajax({
        type: "POST",
        url: "../routes.py"
        // data: ""
    })
}