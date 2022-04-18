const comment_btn = document.getElementById('comment_btn');
comment_btn.addEventListener('click', () => {
    let comment_name = document.getElementById('comment_name');
    let comment_email = document.getElementById('comment_email');
    let comment_text = document.getElementById('comment_text');
    let comment_error = document.getElementById('comments_error');

    if (comment_name.value == '' || comment_email.value == '' || comment_text.value == '') {
        comment_error.innerText = 'Some Fields Are Empty Please Fill!';
        comment_error.style.color = 'red';
    } else {
        const check_comment_email = validateEmail(comment_email.value);
        if (check_comment_email == true) {
            const url = contact_url;
            post_comment(url, {
                name: comment_name.value,
                email: comment_email.value,
                comment: comment_text.value
            }).then(data => {
                // console.log(data.success)
                if (data.success == true) {
                    comment_error.innerText = `${data.message}`
                    comment_error.style.color = 'green'
                    comment_name.value = '';
                    comment_email.value = '';
                    comment_text.value = '';
                } else {
                    comment_error.innerText = `${data.error}`
                    comment_error.style.color = 'red'
                    comment_name.value = '';
                    comment_email.value = '';
                    comment_text.value = '';
                }
            })
        } else {
            comment_error.innerText = 'Invalid Email Please Enter Correct One';
            comment_error.style.color = 'red';
        }
    }
});

function validateEmail(mail) {
    if (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail)) {
        return (true)
    } else {
        return (false)
    }
}

const post_comment = async (url = '', data = {}) => {
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