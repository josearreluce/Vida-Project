const example_symptoms = ['Headache', 'Cough', 'Sneeze', 'Backpain', 'Pain', 'Fever', 'Chills'];

function handleSymptomSearch(res) {
    $('.symptom-container').hide();
    $('.symptom-box-container').removeClass('hidden');
    $('.symptom-box').append("<p class='question'> What is your symptom? </p>");
    $('.symptom-box').append("<p class='answer'>" + res.text + "</p>");
    $('.symptom-box').append("<p class='question'> Do you have any other symptoms? </p>");
    $('.symptom-box').append("<input type='text' class='chat-input'>");

    $.post('/assessment', {
        text: 'Hello Server'
    }).done((res) => {
        console.log(res.text);
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
