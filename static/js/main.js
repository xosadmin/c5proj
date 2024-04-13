function loadLLM(flag) {
    postfix = "";
    if (flag === 1) {
        postfix = "/api/llmrequest";
    }
    else if (flag === 2) {
        postfix = "/api/llmanswer";
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
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
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
                if (email.value.length === 0 || !email.value.includes('@')) {
                    alert('Please enter a valid email address.');
                    isValid = false;
                }
            }

            function validatePassword() {
                const password = document.getElementById('password');
                if (password.value.trim().length === 0) {
                    alert('Password cannot be empty.');
                    isValid = false;
                }
            }
            function validateNewPassword(){
                const password = document.getElementById('newpassword');
                if (newpassword.value.trim().length === 0) {
                    alert('Password cannot be empty.');
                    isValid = false;
                }

            }

            validateEmail();
            validatePassword();

            // Check if the form is the registration form
            if (form.action.includes('/doregister')) {
                function validatePasswordMatch() {
                    const password = document.getElementById('password');
                    const repeatPassword = document.getElementById('repeat-password');
                    if (password.value !== repeatPassword.value) {
                        alert('Passwords do not match.');
                        isValid = false;
                    }
                }
            
            

                function validatePin() {
                    const pin = document.getElementById('pincode');
                    if (!pin || pin.value.trim().length === 0) {
                        alert('PIN cannot be empty.');
                        isValid = false;
                    }
                }

                validatePasswordMatch();
                validatePin();
            }

            if (form.action.includes('/domodifypassword')) {
                function validateNewPasswordMatch() {
                    const newpassword = document.getElementById('newpassword');
                    const repeatnewpassword = document.getElementById('repeatnewpassword');
                    if (newpassword.value !== repeatnewpassword.value) {
                        alert('Passwords do not match.');
                        isValid = false;
                    }
                }
            
            

                function validateNewPin() {
                    const newpin = document.getElementById('newpin');
                    if (!newpin || newpin.value.trim().length === 0) {
                        alert('PIN cannot be empty.');
                        isValid = false;
                    }
                }

                validateNewPasswordMatch();
                validateNewPin();}

            if (!isValid) {
                event.preventDefault();
            }
        });
    });
});



function confirmAcceptRequest(id) {
    var acceptUrl = "/doacceptrequest/" + id;
    window.location.href = acceptUrl;
}

function denyAcceptRequest() {
    window.location.href = "/requests";
}

function confirmPayment(id) {
    var acceptUrl = "/dopayment/" + id;
    window.location.href = acceptUrl;
}

function denyPayment() {
    window.location.href = "/shop";
}