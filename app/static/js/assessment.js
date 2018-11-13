const example_symptoms = ['Symptom_2', 'Symptom_1'];

function handleSuccessors(successors) {
    const symptom_box = $('.symptom-box');
    const symptom_input = $('#symptom-input');

    let i = 0;
    let answers = [];
    symptom_box.append("<p class='question'> Do you have " + successors[i] + "?</p>");
    i += 1;

    symptom_input.keyup((e) => {
        const query = symptom_input.val().toLowerCase();
        if (e.which === 13) {
            if (query === "yes") {
                answers.push(1);
                symptom_box.append("<p class='answer'> Yes </p>");
                symptom_box.append("<p class='question'> Do you have " + successors[i] + "?</p>");
            } else if (query === "no") {
                answers.push(0);
                symptom_box.append("<p class='answer'> No </p>");
                symptom_box.append("<p class='question'> Do you have " + successors[i] + "?</p>");
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
