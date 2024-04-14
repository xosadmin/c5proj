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
        form.addEventListener('doSubmit', function(event) {
            let isValid = true;
            if (form.action.includes('/doregister')) {
                function validatePasswordMatch() {
                    const password = document.getElementById('password');
                    const repeatPassword = document.getElementById('repeat-password');
                    if (password.value !== repeatPassword.value) {
                        alert('Passwords do not match.');
                        isValid = false;
                    }
                }
                validatePasswordMatch();
                validatePin();
            }

            if (form.action.includes('/domodifypassword')) {
                function validateNewPasswordMatch() {
                    const newpassword = document.getElementById('newpassword').value;
                    const repeatnewpassword = document.getElementById('repeatnewpassword').value;
                    if (newpassword !== repeatnewpassword) {
                        alert('Passwords do not match.');
                        isValid = false;
                    }
                }
                validateNewPasswordMatch();
            }

            if (form.action.includes('/domodifypin')){
                function validatePin() {
                    const pin = document.getElementById('newpin').value;
                    const repeatpin = document.getElementById('repeatnewpin').value;
                    if (pin !== repeatpin) {
                        alert('New PIN code mismatch.');
                        isValid = false;
                    }
                }
                validatePin();
            }

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