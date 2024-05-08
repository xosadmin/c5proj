function searchResult(){
    let countryRadio = document.getElementById("country");
    let emailRadio = document.getElementById("email");
    if (countryRadio.checked){
        let type = "country";
        let value = document.getElementById("value").value;
    }
    else if (emailRadio.checked) {
        let type = "email";
        let value = document.getElementById("value").value;
        if (value.indexOf("@") == -1){
            alert("Please insert correct email address.");
            return;
        }
    }
    else {
        alert("Invalid Criteria!");
        return;
    }
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/api/searchuser/" + type + "/" + value);
    xhttp.onload = function() {
        let responseData = JSON.parse(this.responseText);
        displaySearchResults(responseData);
    }
    xhttp.send();
}

function displaySearchResults(results) {
    let tableBody = document.querySelector("#searchResult tbody"); // Choose tbody in searchResult div
    tableBody.innerHTML = ""; // Clear all contents in the table body
    results.forEach(function(user) {
        let row = `
            <tr>
                <td><a href="/profile/${user.id}" title="View User Info" target="_blank">${user.id}</a></td>
                <td><a href="/profile/${user.id}" title="View User Info" target="_blank">${user.email}</a></td>
                <td><a href="/newchat/${user.id}" title="Set This User As Destination User">Set this user</a></td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
    document.getElementById("searchResult").style.display = "block";
    document.getElementById("collapse").style.display = "block";
}


let searchResultCollapse = false;
$(document).ready(function(){
    $("#collapse").click(function(){
        if (searchResultCollapse === false){
            $("#searchResult").hide();
            searchResultCollapse = true;
        }
        else {
            $("#searchResult").show();
            searchResultCollapse = false;
        }
    });
});