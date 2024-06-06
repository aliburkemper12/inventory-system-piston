window.onload = function() {
    getAlert();
    addRowName();
};

function getAlert() {
    console.log("executing")
    var table = document.getElementById("myTable");
    var rows = table.getElementsByTagName("tr");
    var num = 0;
    
    for (var i = 1; i < rows.length; i++) { // start from 1 to skip header row
        var cells = rows[i].getElementsByTagName("td");
        var quantity = parseInt(cells[2].getAttribute("data-quantity"));
        var alert = parseInt(cells[3].getAttribute("data-hidden"));
        
        if (quantity <= alert) {
            num++;
            rows[i].cells[1].style.background = "rgba(255,99,71, 0.6)";
            rows[i].cells[2].style.background = "rgba(255,99,71, 0.6)";
        }
    }
    document.getElementById('replace').innerText = num;
    document.getElementById('alert-a').innerText = " Active Alerts";
}

function addRowName() {
    var table = document.getElementById("myTable");
    var rows = table.getElementsByTagName("tr");
    var previousRow = null;

    for(i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = function(row) {
            return function() {
                if (previousRow !== null) {
                    previousRow.style.backgroundColor = ""; // Reset background color
                }
                
                // Change background color of clicked row
                if (this.style.backgroundColor === "rgba(74, 116, 168)") {
                    this.style.backgroundColor = ""; // Reset to default
                } else {
                    this.style.backgroundColor = "rgba(74, 116, 168)";
                }

                var cell = row.getElementsByTagName("td")[1];
                var id = cell.innerText;

                document.getElementById("small_name").innerText = id;
                document.getElementById("small_name").style.color = "rgb(72, 120, 241)";

                previousRow = this;
            };
        };
        currentRow.onclick = createClickHandler(currentRow);
    }
}


document.addEventListener("DOMContentLoaded", function() {
    console.log('event-listener')
    document.getElementById("name_form").addEventListener("submit", function(event){
        console.log('sending data to flask')
        event.preventDefault(); // Prevent the form from submitting in the traditional way
        
        var name = document.getElementById("small_name").innerText;

        var quantity = document.getElementById("new_small").value;

        var jsonData = JSON.stringify({newText: name, quantity: quantity});
        
        // Send the JSON data to Flask route using AJAX
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/add_small", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(jsonData);

        document.getElementById("small_name").innerText = 'Click Item to Update';
        document.getElementById("small_name").style.color = "";
        document.getElementById("new_small").value = "";
        fetchData();
    });
});

function fetchData() {
    fetch('/add_small', {
        headers: {
            Accept: "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            updateTable(data);
            reapplyScripts();
        })
        .catch(error => {
            console.error('Error getting data', error);
        });
}

function reapplyScripts() {
    addRowName();
    getAlert();
}

function updateTable(data) {
    document.getElementById('myTable').innerHTML = `<tr>
                        <th width="10%" align="left"></th>
                        <th width="50%" align="left">Name<div>
                            <div><form action="{{ url_for("sort_desc")}}" method="post">
                            <input type="hidden" name="name" value="1">
                            <button class="arrow" type="submit"><img src="static/up.png" alt=""></button></form></div>
                            <div><form action="{{ url_for("sort_asc")}}" method="post">
                            <input type="hidden" name="name" value="1">
                            <button class="arrow" type="submit"><img src="static/down.png" alt=""></button></form></div></div>
                        </th>
                        <th width="30%" align="left">Quantity<div>
                            <div><form action="{{ url_for("sort_desc")}}" method="post">
                            <input type="hidden" name="name" value="2">
                            <button class="arrow" type="submit"><img src="static/up.png" alt=""></button></form></div>
                            <div><form action="{{ url_for("sort_asc")}}" method="post">
                            <input type="hidden" name="name" value="2">
                            <button class="arrow" type="submit"><img src="static/down.png" alt=""></button></form></div></div>
                        </th>
                    </tr>`;

    data.forEach(item => {
        let row = `<tr class="data_row" id="data_row">
                        <form action="{{ url_for("edit")}}" method="post">
                        <td width="10%" align="right"><button class="edit" id="count" type="submit"><img src="static/edit_icon.png" alt=""></button></td>
                        <form id="name" method="post">
                        <td width="50%"><input type="hidden" name="name" value="${item.name}">${item.name}</td></form></form>
                        <td width="30%" display="inline-block" id="quantity" data-quantity="${item.quantity}">
                            <form action="/update_q_p" method="post">
                            <input type="hidden" name="name" value="${item.name}">
                            <input type="text" autocomplete="off" class="d_q" name="d_q" placeholder="${item.quantity}"></td></form>
                        <td data-hidden="${item.alert}" style="display:none;"></td></form>
                        <form action="{{ url_for("delete")}}" method="post">
                        <input type="hidden" name="name" value="${item.name}">
                        <td width="auto" align="left"><button class="delete" type="submit"><img src="static/trash.png" alt=""></button></td></form>
                    </tr>`;
        document.getElementById('myTable').innerHTML += row;

        location.reload();
    });
}