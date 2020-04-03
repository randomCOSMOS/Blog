async function test() {
    let form = {
        username: $('#username').val(),
        password: $('#password').val()
    };

    const options = {
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(form)
    };
    const r = await fetch('/test', options);
    const t = await r.json();
    console.log(t)
}

window.addEventListener('keydown',  async (e) => {
    if (e.key === 'l'){
        const response = await fetch('/l');
        const text = await response.text();
        console.log(text);
    }
});