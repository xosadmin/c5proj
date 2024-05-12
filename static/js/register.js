$(document).ready(function(){
    function controlSubmit(flag, value){
        if (flag === 1) { // Disable submit
            let notify = "<p>Submit Disabled: ";
            notify = notify + value + "</p>";
            $("#btnRegister").prop("disabled",true);
            $("#registerErrorDisplay").html(notify);
            $("#registerErrorDisplay").show();
        }
        else if (flag === 2) { // Recover submit button
            $("#btnRegister").prop("disabled",false);
            $("#registerErrorDisplay").hide();
        }
        else {
            console.error("Invalid Flag!");
        }
    }

    $("#repeat_password").on('change',function(){ // Check repeat password
        let passwordValue = $("#password").val();
        let repeatValue = $(this).val();
        if (passwordValue !== repeatValue){
            let notify = "The password is not equal to repeat password.";
            controlSubmit(1,notify);
        }
        else {
            controlSubmit(2,"");
        }
    });
});
