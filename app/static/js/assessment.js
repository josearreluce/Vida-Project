const example_symptoms = ['Symptom_2', 'Symptom_1'];

function sendSuccessors(answers) {
    console.log("Sending Successors");
    $("#symptom-input").off('keyup');
    console.log(answers);

    const data = {"answers": answers};
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/successors',
        dataType : 'json',
        data : JSON.stringify(data),
        success : function(result) {
            console.log(result);
            const condition_elem = $("<p class='question'> Congratulations! You have " + result.conditions[0][0] + "</p>");
            $(condition_elem).insertBefore($("#symptom-input"));
        },error : function(result){
            console.log("ERROR");
        }
    });
}

function handleSuccessors(successors) {
    const symptom_box = $('.symptom-box');
    const symptom_input = $('#symptom-input');

    var i = 0;
    let answers = [];

    //symptom_box.append("<p class='question'> Do you have " + successors[i] + "?</p>");
    const newElem = "<p class='question'> Do you have " + successors[i] + "?</p>";
    $(newElem).insertBefore(symptom_input);
    i += 1;

    symptom_input.on("keyup", (e) => {
        const query = symptom_input.val().toLowerCase();
        if (e.which === 13) {
            symptom_input.val('');
            let is_good_answer = false;
            let answer = '';
            if (query === "yes" || query === "no") {
                answer = query;
                answers.push(query === "yes");
                is_good_answer = true;
            }

            if (is_good_answer) {
                const new_answer = "<p class='answer'>" + answer + "</p>";
                $(new_answer).insertBefore(symptom_input);

                if (i + 1 > successors.length) {
                    sendSuccessors(answers);
                } else {
                    const new_question = "<p class='question'> Do you have " + successors[i] + "?</p>";
                    $(new_question).insertBefore(symptom_input);
                }

                i += 1;
            }
        }
    });
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
