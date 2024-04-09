function loadLLM(flag) {
    postfix = "";
    if (flag === 1) {
        postfix = "/llmrequest";
    }
    else if (flag === 2) {
        postfix = "/llmanswer";
    }
    else {
        console.error("Invalid input!");
    }
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.getElementById("content").innerHTML = this.responseText;
    }
    xhttp.open("GET", postfix);
    xhttp.send();
} 
    
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    form.addEventListener('doSubmit', function(event) {
        let isValid = true;
        function checkNotEmpty(inputId, message) {
            const input = document.getElementById(inputId);
            if (!input || input.value.trim().length === 0) {
                alert(message);
                isValid = false;
            }
        }
        
        function validateEmail() {
            const email = document.getElementById('email');
            if (email && (email.value.length === 0 || !email.value.includes('@'))) {
                alert('Please enter a valid email address.');
                isValid = false;
            }
        }

        function validatePasswordLength() {
            const password = document.getElementById('password');
            if (password && password.value.length < 8) {
                alert('Password must be at least 8 characters long.');
                isValid = false;
            }
        }

        function validatePasswordMatch() {
            const password = document.getElementById('password');
            const repeatPassword = document.getElementById('repeat-password');
            if (password && repeatPassword && password.value !== repeatPassword.value) {
                alert('Passwords do not match.');
                isValid = false;
            }
        }
       
        validateEmail();
        validatePasswordLength();

        if (document.getElementById('repeat-password') !== null) {
            validatePasswordMatch();
        }

        checkNotEmpty('content', 'Content cannot be empty.');
        checkNotEmpty('title', 'Title cannot be empty.');
        checkNotEmpty('rewards', 'Rewards cannot be empty.');
        checkNotEmpty('timelimit', 'Time Limit cannot be empty.');

        if (!isValid) {
            event.preventDefault();
        }
    });
});