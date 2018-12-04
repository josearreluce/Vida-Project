// Scroll the input into view regardless of number of questions and answers
function scrollToInput() {
    const input_pos = document.getElementById("yes").offsetTop;
    const assessment_container = document.getElementsByClassName("symptom-assessment final")[0];
    assessment_container.scrollTop = input_pos - 10;
}

/**
 * Turns off the event listener on the symptom input box and sends an ajax request
 * to the server with the user's answers to whether or not they have each of the successor
 * symptoms. Expects a list of conditions organized by probability from the server/back-end.
 *
 * @param answers
 */
function sendSuccessors(answers) {
    $("#symptom-input").off('keyup');
    console.log(answers);
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
            scrollToInput();
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
    const answer_container = $('.button-answers');

    var i = 0;
    let answers = [];

    const newElem = "<p class='question'> Do you have " + successors[i] + "?</p>";

    $(newElem).insertBefore(answer_container);

    i += 1;

    const answer_buttons = $(".answer-buttons");
    answer_buttons.on("click", (e) => {
        console.log(e.target.id);
        const answer = e.target.id;
        answers.push(answer === 'yes');
        if (i + 1 > successors.length) {
            sendSuccessors(answers);
        } else {
            const new_answer = `<p class='answer'> ${answer} </p>`;
            const new_question = `<p class='question'> Are you experiencing ${successors[i]}? </p>`;

            $(new_answer).insertBefore(answer_container);
            $(new_question).insertBefore(answer_container);

            scrollToInput();
            i += 1;
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

    symptom_box.append("<div class='button-answers' style='display: flex;'>");
    const answer_input = $('.button-answers');
    answer_input.append("<button class='answer-buttons' id='yes'> Yes </button>");
    answer_input.append("<button class='answer-buttons' id='no'> No </button>");
    answer_input.append("<button class='answer-buttons' id='skip'> Skip </button>");

    $.post('/assessment', {
        data: res.text
    }).done((res) => {
        handleSuccessors(res.successors);
    }).fail(() => {
        console.log("Failure");
    });
}

$('#symptom-search').keyup((e) => {
    // Get the current value of the user input and save as query.
    let query = $("#symptom-search").val().toLowerCase();

    // Get all symptoms that match/begin with input query
    let results = [];
    const example_symptoms =   ["abdominal pain",
                                "indigestion",
                                "diarrhea",
                                "change in bowel habits",
                                "loss of appetite",
                                "nausea",
                                "fever",
                                "fatigue",
                                "itchiness",
                                "eye itchiness",
                                "vertigo",
                                "sore throat",
                                "irritability",
                                "thirst",
                                "mental confusion",
                                "loss of muscle function",
                                "missed period",
                                "light spotting",
                                "increased sensitivity",
                                "pus",
                                "blood in stool",
                                "dilated pupils",
                                "body ache",
                                "malaise",
                                "itchy nose",
                                "shortness of breath",
                                "bulging in groin",
                                "changes in urination",
                                "inflammation of ear",
                                "headache",
                                "pain in face",
                                "testicular pain",
                                "tenderness",
                                "cough",
                                "congestion"];

    if (query.length > 0) {
        example_symptoms.forEach((symptom) => {
            const curr_symptom = symptom.toLowerCase();
            if (curr_symptom.startsWith(query)) {
                results.push(symptom);
            }
        });
    }

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