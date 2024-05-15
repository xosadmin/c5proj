function loadLLM(url) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, false); // false = Make HTTP request synchronized
    xhttp.send();

    if (xhttp.status === 200) {
        return xhttp.responseText;
    }
    else {
        console.error("Error while loading " + url);
        return null;
    }
}

$(document).ready(function(){
    $("#llmSigns").on("click", function(){
        let url = "/api/feelingsllm";
        let data = loadLLM(url);
        if (data !== null) {
            $("#content").val(data);
        }
    });

    $("#llmRequest").on("click", function(){
        let url = "/api/llmrequest";
        let data = loadLLM(url);
        if (data !== null) {
            $("#content").val(data);
        }
    });

    $("#llmAnswer").on("click", function(){
        let url = "/api/llmanswer";
        let data = loadLLM(url);
        if (data !== null) {
            $("#content").val(data);
        }
    });
});
