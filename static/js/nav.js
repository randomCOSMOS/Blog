$('.hamburger').click(() => {
    $('.hamburger').toggleClass('is-active');
    $('nav div').toggleClass('show');
});

let op = window.location.href;
console.log(op.indexOf('localhost'));

if ((window.location.href).indexOf('localhost') !== 7) {
    let loc = window.location.href + '';
    if (loc.indexOf('http://') === 0) {
        window.location.href = loc.replace('http://', 'https://');
    }
}