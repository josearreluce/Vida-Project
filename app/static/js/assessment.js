const example_symptoms = ['Symptom_2', 'Symptom_1'];

//var i = 0;

function sendSuccessors(answers) {
    console.log("Sending Successors");
    $("#symptom-input").off('keyup');
    console.log(answers);
    /*
    $.ajax({
        type: "POST",
        url: "/successors",
        data: answers,
        success: function(data){
            console.log("SUCCEED");
        },
        failure: function(data) {
            console.log("FAILURE");
        }
    }); */
    //var data = {"name":"John Doe","age":"21"};
    const data = {"answers": answers};
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/successors',
        dataType : 'json',
        data : JSON.stringify(data),
        success : function(result) {
            console.log(result);
        },error : function(result){
            console.log("ERROR");
        }
    });
    /*
    $.post('/successors', {
        data: {'answers': answers}
    }).done((res) => {
       console.log(res.conditions);
    }).fail(() => {
        console.log("Failure");
    });
    */
}

function handleSuccessors(successors) {
    const symptom_box = $('.symptom-box');
    const symptom_input = $('#symptom-input');

    var i = 0;
    let answers = [];
    symptom_box.append("<p class='question'> Do you have " + successors[i] + "?</p>");
    i += 1;

    symptom_input.on("keyup", (e) => {
        const query = symptom_input.val().toLowerCase();
        if (e.which === 13) {
            let is_good_answer = false;
            let answer = '';
            if (query === "yes") {
                answer = "Yes";
                is_good_answer = true;
                answers.push(1);
            } else if (query === "no") {
                answer = "No";
                is_good_answer = true;
                answers.push(0);
            }

            if (is_good_answer) {
                symptom_box.append("<p class='answer'>" + answer + "</p>");
                symptom_box.append("<p class='question'> Do you have " + successors[i] + "?</p>");
                i += 1;

                if (i > successors.length) {
                    sendSuccessors(answers);
                }
            }
        }
    });

    /*
    const interval = setInterval(() => {
        if (i >= successors.length) {
            $("#symptom-input").off("keyup");
            console.log("Turn off event listener");
        }

        console.log(i);
    }, 500);
    */
}


function handleSymptomSearch(res) {
    $('.symptom-container').hide();
    $('.symptom-box-container').removeClass('hidden');
    $("main").removeClass("initial-assessment");

    const symptom_box = $('.symptom-box');
    symptom_box.append("<p class='question'> What is your symptom? </p>");
    symptom_box.append("<p class='answer'>" + res.text + "</p>");
    symptom_box.append("<input type='text' class='chat-input' id='symptom-input' />");

    $.post('/assessment', {
        data: res.text
    }).done((res) => {
        console.log("SUCCESS 1");
        handleSuccessors(res.successors);
    }).fail(() => {
        console.log("Failure");
    });
}

let query = '';
$('#symptom-search').keyup((e) => {
    // Update the query for search only if alphabetic character
    let query = $("#symptom-search").val().toLowerCase();

    let results = [];
    example_symptoms.forEach((symptom) => {
        const curr_symptom = symptom.toLowerCase();
        if (curr_symptom.startsWith(query)) {
            results.push(symptom);
        }
    });

    $('.symptom-results').empty();
    results.forEach((res) => {
        $('.symptom-results').append(
            "<a id='" + res + "' class='symptom-result'>" + res + "<\a>"
        );
    });

    $('.symptom-result').click((e) => {
        handleSymptomSearch(e.target);
    });

    if (e.which === 13) {
        if (results.length > 0) {
            const res = document.getElementById(results[0]);
            handleSymptomSearch(res);
        }
    }
});
