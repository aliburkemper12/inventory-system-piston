window.onload = function() {
    getAlert();
};

function getAlert() {
    console.log("executing")
    var table = document.getElementById("myTable");
    var rows = table.getElementsByTagName("tr");
    
    for (var i = 1; i < rows.length; i++) { // start from 1 to skip header row
        var cells = rows[i].getElementsByTagName("td");
        var quantity = parseInt(cells[2].getAttribute("data-quantity"));
        var alert = parseInt(cells[6].getAttribute("data-hidden"));
        
        if (quantity <= alert) {
            rows[i].cells[1].style.background = "rgba(255,99,71, 0.6)";
            rows[i].cells[2].style.background = "rgba(255,99,71, 0.6)";
            rows[i].cells[3].style.background = "rgba(255,99,71, 0.6)";
            rows[i].cells[4].style.background = "rgba(255,99,71, 0.6)";
            rows[i].cells[5].style.background = "rgba(255,99,71, 0.6)";
        }
    }
}