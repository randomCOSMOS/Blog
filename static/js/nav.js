$('.hamburger').click(() => {
    $('.hamburger').toggleClass('is-active');
    $('nav div').toggleClass('show');
});

// var loc = window.location.href + '';
// if (loc.indexOf('http://') == 0) {
//     window.location.href = loc.replace('http://', 'https://');
// }