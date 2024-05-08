function loadLLM(flag) {
    postfix = "";
    if (flag === 1) {
        postfix = "/api/llmrequest";
    }
    else if (flag === 2) {
        postfix = "/api/llmanswer";
    }
    else if (flag === 3) {
        postfix = "/api/feelingsllm";
    }
    else {
        console.error("Invalid input!");
    }
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", postfix);
    xhttp.onload = function() {
        document.getElementById("content").innerHTML = this.responseText;
    }
    xhttp.send();
}

$(document).ready(function(){
    let showpinExpand = false;
    $('#showpin').click(function(){
        if (showpinExpand === false){
            $('#pincode').show();
            showpinExpand = true;
        }
        else {
            $('#pincode').hide();
            showpinExpand = false;
        }
    });
});

function confirmAcceptRequest(id) {
    let acceptUrl = "/doacceptrequest/" + id;
    window.location.href = acceptUrl;
}

function denyAcceptRequest() {
    window.location.href = "/requests";
}

function confirmPayment(id) {
    let acceptUrl = "/dopayment/" + id;
    window.location.href = acceptUrl;
}

function denyPayment() {
    window.location.href = "/shop";
}