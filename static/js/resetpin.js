document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log("Received form.");
            const newpassword = document.getElementById("newpin").value;
            const repeatnewpassword = document.getElementById("repeatnewpin").value;
            if (newpassword.length < 4) {
                console.error("PIN code cannot be less than 4 characters");
                alert("PIN code cannot be less than 4 characters");
                event.preventDefault();
                return;
            }
            if (newpassword !== repeatnewpassword) {
                console.error("Password mismatch!");
                alert("PIN/Password Mismatch!");
                event.preventDefault();
                return;
            }
        });
    });
});
