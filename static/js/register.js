document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Received form.");
            password = document.getElementById("password").value;
            repeatpassword = document.getElementById("repeat-password").value;
            pincode = document.getElementById("pin-code").value;
            if (password !== repeatpassword) {
                console.error("Password mismatch!");
                alert("Password mismatch!");
                event.preventDefault();
            }
            if (pincode.length < 4) {
                console.error("PIN code cannot less than 4 letters");
                alert("PIN code cannot less than 4 letters");
                event.preventDefault();
            }
        });
    });
});
