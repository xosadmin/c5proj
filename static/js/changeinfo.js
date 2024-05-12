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
                alert("Email addresses are mismatch!");
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
            alert("Passwords are mismatch!");
            return false;
        }
        else if (newpassword.length < 4 || newpassword.length > 32) {
            alert("Password cannot lower than 4 or larger than 32 characters.");
            return false;
        }
        else {
            return true;
        }
    }
    else if (type === "pin") {
        const newpin = document.getElementById("newpin").value;
        const repeatnewpin = document.getElementById("repeatnewpin").value;
        if (newpin.length < 4) {
            alert("PIN code cannot be less than 4 digits");
            return false;
        }
        else if (newpin !== repeatnewpin) {
            alert("PINs are mismatch!");
            return false;
        }
        else {
            return true;
        }
    }
}
