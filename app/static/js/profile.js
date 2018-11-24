$(document).ready(() => {
    console.log("Document is ready.");
    $('.edit-profile-info').click(() => {
        $('.profile-editor').show();
        $('.profile-info').hide();
    });
});