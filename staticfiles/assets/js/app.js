const subscribe_btn = document.getElementById('subscribe_btn');
subscribe_btn.addEventListener('click', async () => {
    var input_email = document.getElementById('input_subscribe_email').value;
    var email_error = document.getElementById('email_error');
    let check_email = validateEmail(input_email);
    if (check_email == true) {
        const url = 'http://127.0.0.1:8000/api/home/subscibe';
        await post_subscribe_email(url, {email: input_email}).then(data => {
            // console.log(data);
            if (data.success == true) {
                email_error.innerText = `${data.message}`
                email_error.style.color = 'green'
                input_email = '';
            } else {
                email_error.innerText = `${data.errors}`
                email_error.style.color = 'red'
                input_email.value = '';
            }
        });

    } else {
        email_error.innerText = "You have entered an invalid email address!"
        email_error.style.color = 'red'
    }
});

const post_subscribe_email = async (url = '', data = {}) => {
    const res = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(data)
    });
    const res_data = await res.json();
    return res_data;
}

function validateEmail(mail) {
    if (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail)) {
        return (true)
    } else {
        return (false)
    }
}
