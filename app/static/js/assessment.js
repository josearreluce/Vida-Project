const example_symptoms = ['Headache', 'Cough', 'Sneeze', 'Backpain', 'Pain', 'Fever', 'Chills'];

let query = '';
$('.input').keyup((e) => {
    // Update the query for search only if alphabetic character
    let query = $(".input").val();
    console.log(query);

    let results = [];
    example_symptoms.forEach((symptom) => {
       if (symptom.startsWith(query)) {
           results.push(symptom);
       }
    });

    $('.symptom-results').empty();
    results.forEach((res) => {
        $('.symptom-results').append(
            "<li class='symptom-result'>" + res + "<\li>"
        );
    });
});
