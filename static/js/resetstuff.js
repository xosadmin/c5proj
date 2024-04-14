document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Received form.");
            newpassword = document.getElementById("newpassword").value;
            repeatnewpassword = document.getElementById("repeatnewpassword").value;
            if (newpassword === "" && repeatnewpassword === "") {
                newpassword = document.getElementById("newpin").value;
                repeatnewpassword = document.getElementById("repeatnewpin").value;
                pincode = document.getElementById("pincode").value;
                if (pincode.length < 4) {
                    console.error("PIN code cannot less than 4 letters");
                    alert("PIN code cannot less than 4 letters");
                    event.preventDefault();
                }
            }
            if (password !== repeatpassword) {
                console.error("Password mismatch!");
                event.preventDefault();
            }
        });
    });
});
