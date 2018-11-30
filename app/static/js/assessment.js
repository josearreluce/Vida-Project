const example_symptoms = ['sympt_1', 'sympt_10', 'sympt_11', 'sympt_12', 'sympt_13', 'sympt_14', 'sympt_15', 'sympt_16', 'sympt_17', 'sympt_18', 'sympt_19', 'sympt_2', 'sympt_20', 'sympt_21', 'sympt_22', 'sympt_23', 'sympt_24', 'sympt_25', 'sympt_26', 'sympt_27', 'sympt_28', 'sympt_29', 'sympt_3', 'sympt_30', 'sympt_31', 'sympt_32', 'sympt_33', 'sympt_34', 'sympt_35', 'sympt_4', 'sympt_5', 'sympt_6', 'sympt_7', 'sympt_8', 'sympt_9'];

/**
 * Turns off the event listener on the symptom input box and sends an ajax request
 * to the server with the user's answers to whether or not they have each of the successor
 * symptoms. Expects a list of conditions organized by probability from the server/back-end.
 *
 * @param answers
 */
function sendSuccessors(answers) {
    $("#symptom-input").off('keyup');

    const data = {"answers": answers};
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/successors',
        dataType : 'json',
        data : JSON.stringify(data),
        success : (res) => {
            const condition_elem = $(
                "<p class='question'> You have " +
                res.conditions[0][0] +
                "</p>");

            $(condition_elem).insertBefore($("#symptom-input"));
        },error : (res) => {
            console.log("ERROR");
        }
    });
}

/**
 *
 * @param successors
 */
function handleSuccessors(successors) {
    const symptom_input = $('#symptom-input');

    var i = 0;
    let answers = [];

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

/**
 *
 * @param res
 */
function handleSymptomSearch(res) {
    $('.symptom-assessment__initial').hide();
    $("main").removeClass("initial-assessment");

    const symptom_container = $(".symptom-container");
    const symptom_assessment = $('.symptom-assessment');

    symptom_container.removeClass("initial-assessment");
    symptom_container.addClass("final-assessment");

    symptom_assessment.removeClass('initial');
    symptom_assessment.addClass('final');

    const symptom_box = $('.symptom-assessment__final');
    symptom_box.append("<p class='question'> What is your symptom? </p>");
    symptom_box.append("<p class='answer'>" + res.text + "</p>");
    symptom_box.append("<input type='text' class='chat-input' id='symptom-input' />");

    $.post('/assessment', {
        data: res.text
    }).done((res) => {
        handleSuccessors(res.successors);
        draw();
    }).fail(() => {
        console.log("Failure");
    });
}

$('#symptom-search').keyup((e) => {
    // Get the current value of the user input and save as query.
    let query = $("#symptom-search").val().toLowerCase();

    // Get all symptoms that match/begin with input query
    let results = [];
    const example_symptoms = ['sympt_1', 'sympt_10', 'sympt_11', 'sympt_12', 'sympt_13', 'sympt_14', 'sympt_15', 'sympt_16', 'sympt_17', 'sympt_18', 'sympt_19', 'sympt_2', 'sympt_20', 'sympt_21', 'sympt_22', 'sympt_23', 'sympt_24', 'sympt_25', 'sympt_26', 'sympt_27', 'sympt_28', 'sympt_29', 'sympt_3', 'sympt_30', 'sympt_31', 'sympt_32', 'sympt_33', 'sympt_34', 'sympt_35', 'sympt_4', 'sympt_5', 'sympt_6', 'sympt_7', 'sympt_8', 'sympt_9'];
    example_symptoms.forEach((symptom) => {
        const curr_symptom = symptom.toLowerCase();
        if (curr_symptom.startsWith(query)) {
            results.push(symptom);
        }
    });

    // Update symptom-results div to contain the matching symptoms
    $('.symptom-results').empty();
    results.forEach((res) => {
        $('.symptom-results').append(
            createSymptomResult(res)
        );
    });

    // Add event listener for click event to all symptom results.
    $('.symptom-result').click((e) => {
        handleSymptomSearch(e.target);
    });

    // If user presses enter button, if there are matching symptoms for input, send symptom to back-end.
    if (e.which === 13) {
        if (results.length > 0) {
            const res = document.getElementById(results[0]);
            handleSymptomSearch(res);
        }
    }
});

function createSymptomResult(symptom_name) {
    return "<a id='" + symptom_name + "' class='symptom-result'>" + symptom_name + "<\a>"
}