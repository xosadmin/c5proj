$(document).ready(function(){
    $("#repeat_password").on('change',function(){
        var passwordValue = $("#password").val();
        var repeatValue = $(this).val();
        if (passwordValue !== repeatValue){
            $("#dosubm").prop("disabled",true);
            $("#whydisableSubButt").html("<p>Submit Disabled: The password is not equal to repeat password.</p>");
            $("#whydisableSubButt").show();
            alert("Password Mismatch!");
        }
        else {
            $("#dosubm").prop("disabled",false);
            $("#whydisableSubButt").hide();
        }
    });
});
