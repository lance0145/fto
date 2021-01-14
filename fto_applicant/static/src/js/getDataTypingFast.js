function checkClassChangesOnTyping() {
    /*if (window.location.href.indexOf('nwpm=') > 0) {
        var typingData = document.getElementById("if1").contentWindow.location.href;
        var typingResult = typingData.split('&');
        var typingSpeed = typingResult[1].replace("nwpm=", "");
        return typingSpeed;
    }*/
    var e = document.getElementsByClassName("amount")[0];
    if (e.length > 0){
        var typingSpeed = e.innerText;
        //console.log(typingSpeed);
        return typingSpeed;
    }
    else{
        setTimeout(checkClassChangesOnTyping, 30000);
    }
}

function checkClassChangesOnFast(){
    var e = document.getElementById("speed-value");
    if (e.className == 'speed-results-container succeeded'){
        var internetSpeed = e.innerText;
        //console.log(internetSpeed);
        return internetSpeed;
    }
    else{
        setTimeout(checkClassChangesOnFast, 10000);
    }
}

function getSpeedResult(){
    try {  
        var res = (checkClassChangesOnFast() ? checkClassChangesOnFast() : '0');
        $("#assessments_details_content input[name='x_test_speed_results']").val(res);
    } catch(err) {
        console.log(err);
    }
}

function getTypingResult(){
    try {  
        var res = (checkClassChangesOnTyping() ? checkClassChangesOnTyping() : '0');
        $("#assessments_details_content input[name='x_test_type_results']").val(res);
    } catch(err) {
        console.log(err);
    }
}