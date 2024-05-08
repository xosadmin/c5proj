$(document).ready(function(){
    function controlSubmit(flag, value){
        if (flag === 1) { // Disable submit
            let notify = "<p>Submit Disabled: ";
            notify = notify + value + "</p>";
            $("#dosubm").prop("disabled",true);
            $("#whydisableSubButt").html(notify);
            $("#whydisableSubButt").show();
        }
        else if (flag === 2) { // Recover submit button
            $("#dosubm").prop("disabled",false);
            $("#whydisableSubButt").hide();
        }
        else {
            console.error("Invalid Flag!");
        }
    }

    $("#email").on('change',function(){
        let emailInput = $("#email").val();
        if (emailInput.indexOf("@") === -1 || emailInput.indexOf(".") === -1) { // If user input invalid email address
            let notify = "Invalid Email Address!";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });

    $("#pin_code").on('change',function(){
        let pincodeInput = $("#pin_code").val();
        if (pincodeInput.length < 4) {
            let notify = "Invalid PIN Code!";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });

    $("#password").on('change',function(){
        let passwordValue = $("#password").val();
        if (passwordValue.length < 4){
            let notify = "The password cannot lower than 4 words.";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });

    $("#repeat_password").on('change',function(){ // Check repeat password
        let passwordValue = $("#password").val();
        let repeatValue = $(this).val();
        if (passwordValue !== repeatValue){
            let notify = "The password is not equal to repeat password.";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });
});
