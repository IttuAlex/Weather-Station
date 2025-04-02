document.addEventListener("DOMContentLoaded", function() {
    const signupBtn = document.querySelector('#singup');
    if (signupBtn) {
        signupBtn.addEventListener('click', function() {
            window.location.href = 'signup.html';
        });
    } else {
        console.error("Butonul #singup nu a fost gasit!");
    }

    const registerBtn = document.querySelector('#registerBtn');
    if (registerBtn) {
        registerBtn.addEventListener('click', function() {
            const emailSign = document.querySelector('#typeEmail');
            const passwordSign = document.querySelector('#typePassword');
            const passwordSignConfirm = document.querySelector('#typePassword2');
            
            const email = emailSign.value.trim();
            const password = passwordSign.value.trim();
            const passwordConfirm = passwordSignConfirm.value.trim();

            if (password !== passwordConfirm) {
                alert("Parolele nu sunt la fel!");
                return;
            }

            const apiUrl = 'http://100.72.182.23:5001/register';

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Email-ul este deja folosit!");
                    return;
                }

                alert("Inregistrare reusita!");
                window.location.href = '../index.html';
            })
            .catch(error => {
                console.error('A aparut o eroare:', error);
            });
        });
    }

    const loginBtn = document.querySelector('#loginacces');
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            const emailLogin = document.querySelector('#typeEmail');
            const passwordLogin = document.querySelector('#typePassword');
            
            const email = emailLogin.value.trim();
            const password = passwordLogin.value.trim();

            const apiUrl = 'http://100.72.182.23:5001/login';

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            })
            .then(response => response.json())
            .then(data => {
                
                console.log('Raspuns server:', data);

                if (data.error) {
                    alert("Email sau parola incorecta!");
                    return;
                }

                window.location.href = '../index.html';  

            })
            .catch(error => {
                console.error('A aparut o eroare:', error);
            });
        });
    }
});
