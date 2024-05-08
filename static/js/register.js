$(document).ready(function(){
    function controlSubmit(flag, value){
        if (flag === 1) { // Disable submit
            const notify = "<p>Submit Disabled: ";
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
        const emailInput = $("#email").val();
        if (emailInput.indexOf("@") === -1 || emailInput.indexOf(".") === -1) { // If user input invalid email address
            const notify = "Invalid Email Address!";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });

    $("#pin_code").on('change',function(){
        const pincodeInput = $("#pin_code").val();
        if (pincodeInput.length < 4) {
            const notify = "Invalid PIN Code!";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });

    $("#repeat_password").on('change',function(){ // Check repeat password
        const passwordValue = $("#password").val();
        const repeatValue = $(this).val();
        if (passwordValue !== repeatValue){
            const notify = "The password is not equal to repeat password.";
            controlSubmit(1,notify);
            alert(notify);
        }
        else {
            controlSubmit(2,"");
        }
    });
});
