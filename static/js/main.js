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
    const acceptUrl = "/doacceptrequest/" + id;
    window.location.href = acceptUrl;
}

function denyAcceptRequest() {
    window.location.href = "/requests";
}

function confirmPayment(id) {
    const acceptUrl = "/dopayment/" + id;
    window.location.href = acceptUrl;
}

function denyPayment() {
    window.location.href = "/shop";
}