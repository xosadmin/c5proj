document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Received form.");
            let password = document.getElementById("password").value;
            let repeatPassword = document.getElementById("repeat_password").value;
            let pinCode = document.getElementById("pin_code").value;
            if (password !== repeatPassword) {
                console.error("Password mismatch!");
                alert("Password mismatch!");
                event.preventDefault();
            }
        });
    });
});