document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Received form.");
            newpassword = document.getElementById("newpassword").value;
            repeatnewpassword = document.getElementById("repeatnewpassword").value;
            if (newpassword !== repeatnewpassword) {
                console.error("Password mismatch!");
                alert("PIN/Password Mismatch!");
                event.preventDefault();
            }
        });
    });
});
