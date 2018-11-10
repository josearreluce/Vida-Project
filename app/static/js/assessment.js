const example_symptoms = ['Headache', 'Cough', 'Sneeze', 'Backpain', 'Pain', 'Fever', 'Chills'];

let query = '';
$('.input').keydown((e) => {
    // Update the query for search only if alphabetic character
    if (e.which >= 65 && e.which <=90) {
        query += String.fromCharCode(e.which);
    }

    if (e.which === 8) {
        query = query.slice(0, -1);
    }
});
