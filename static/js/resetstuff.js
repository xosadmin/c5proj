document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Received form.");
            let newpassword,repeatnewpassword,pincode;

            const newPasswordElem = document.getElementById("newpassword");
            if (newPasswordElem){ //Modify password page
                newpassword = newPasswordElem.value;
                repeatnewpassword = document.getElementById("repeatnewpassword").value;
                pincode = "0"; // Disable pincode check by Javascript
            }

            const newPinElem = document.getElementById("newpin")
            if (newPinElem) { //Modify pin page
                newpassword = newPinElem.value;
                repeatnewpassword = document.getElementById("repeatnewpin").value;
                pincode = document.getElementById("pincode").value;
                if (pincode.length < 4) {
                    console.error("PIN code cannot be less than 4 letters");
                    alert("PIN code cannot be less than 4 letters");
                    event.preventDefault();
                    return;
                }
            }
            if (newpassword !== repeatnewpassword) {
                console.error("Password mismatch!");
                alert("PIN/Password Mismatch!");
                event.preventDefault();
            }
        });
    });
});
