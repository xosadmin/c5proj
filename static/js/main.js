function loadLLM(flag) {
    postfix = "";
    if (flag === 1) {
        postfix = "/llmrequest";
    }
    else if (flag === 2) {
        postfix = "/llmanswer";
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
} // flag: 1 - LLM for requests; 2 - LLM for answer requests