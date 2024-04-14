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