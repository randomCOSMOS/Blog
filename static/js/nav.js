$('.hamburger').click(() => {
    $('.hamburger').toggleClass('is-active');
    $('nav div').toggleClass('show');
});

if ((window.location.href).indexOf('localhost') !== 7) {
    let loc = window.location.href + '';
    if (loc.indexOf('http://') === 0) {
        window.location.href = loc.replace('http://', 'https://');
    }
}