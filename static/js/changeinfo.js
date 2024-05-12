$(document).ready(function(){
    let lastExpand = "None"; // Avoid from form overlap
    $("#chooseChangeEmail").click(function(){
        $(lastExpand).hide();
        $("#emailChange").show();
        $("#type").val("email");
        lastExpand = "#emailChange";
    });
    $("#chooseChangeCountry").click(function(){
        $(lastExpand).hide();
        $("#countryChange").show();
        $("#type").val("country");
        lastExpand = "#countryChange";
    });
    $("#chooseChangePassword").click(function(){
        $(lastExpand).hide();
        $("#passwordChange").show();
        $("#type").val("password");
        lastExpand = "#passwordChange";
    });
    $("#chooseChangePin").click(function(){
        $(lastExpand).hide();
        $("#pinChange").show();
        $("#type").val("pin");
        lastExpand = "#pinChange";
    });
    $("#submitInfo").show(); // Show submit button
});

function checkSubmittedForm(){
    let type = document.getElementById("type").value;
    if (type === "email"){
        const newEmail = document.getElementById("newEmail").value;
        const repeatNewEmail = document.getElementById("repeatNewEmail").value;
        if (newEmail.indexOf("@") !== -1 && newEmail.indexOf(".") !== -1) {
            if (newEmail === repeatNewEmail) {
                return true;
            }
            else {
                alert("Email Address Mismatch!");
                return false;
            }
        }
        else {
            alert("Invalid Email Address!");
            return false;
        }
    }
    else if (type === "country") {
        const country = document.getElementById("country").value;
        if (country !== "") {
            return true;
        }
        else {
            alert("Country cannot be empty!");
            return false;
        }
    }
    else if (type === "password") {
        const newpassword = document.getElementById("newpassword").value;
        const repeatnewpassword = document.getElementById("repeatnewpassword").value;
        if (newpassword !== repeatnewpassword) {
            alert("PIN/Password Mismatch or invalid PIN!");
            return false;
        }
        else if (newpassword.length < 4 || newpassword.length > 32) {
            alert("Password cannot lower than 4 or larger than 32 words.");
            return false;
        }
        else {
            return true;
        }
    }
    else if (type === "pin") {
        const newpassword = document.getElementById("newpin").value;
        const repeatnewpassword = document.getElementById("repeatnewpin").value;
        if (newpassword.length < 4) {
            alert("PIN code cannot be less than 4 characters");
            return false;
        }
        else if (newpassword !== repeatnewpassword) {
            alert("PIN/Password Mismatch!");
            return false;
        }
        else {
            return true;
        }
    }
}
