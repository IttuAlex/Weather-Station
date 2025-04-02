document.addEventListener("DOMContentLoaded", function() {
    const API_BASE_URL = ''; 

    const loginBtn = document.querySelector('.loginbtn');
    const loggedInMessage = document.getElementById('loggedInMessage');
    const stationsLink = document.getElementById('stations');
    const refreshBtn = document.getElementById('refreshBtn');

    async function checkSession() {
        try {
            const response = await fetch(`/check_session`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 401) {
                localStorage.removeItem('user');
                return { logged_in: false };
            }

            if (!response.ok) {
                throw new Error(`Eroare server: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Eroare la verificarea sesiunii:', error);
            return { logged_in: false };
        }
    }

    async function updateAuthUI() {
        const sessionData = await checkSession();
        const userData = JSON.parse(localStorage.getItem('user'));

        const isAuthenticated = sessionData.logged_in && userData && userData.email;
        if (loginBtn) {
            loginBtn.style.display = isAuthenticated ? 'none' : 'block';
        }

        if (loggedInMessage) {
            loggedInMessage.style.display = isAuthenticated ? 'block' : 'none';
            if (isAuthenticated) {
                loggedInMessage.textContent = `Bine ai venit, ${userData.email}!`;
            }
        }

        return isAuthenticated;
    }

    updateAuthUI().then(authenticated => {
        console.log('Stare autentificare initiala:', authenticated);
    });

    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            window.location.href = 'src/login.html';
        });
    }

    if (stationsLink) {
        stationsLink.addEventListener('click', async function(e) {
            e.preventDefault();
            try {
                const isAuthenticated = await updateAuthUI();
                if (isAuthenticated) {
                    window.location.href = 'statii.html';
                } else {
                    alert('Trebuie sa te autentifici mai intai!');
                    window.location.href = 'src/login.html';
                }
            } catch (error) {
                console.error('Eroare la navigare:', error);
                alert('Eroare la verificarea autentificarii');
            }
        });
    }

    if (refreshBtn) {
        refreshBtn.addEventListener('click', async function() {
            try {
                const response = await fetch(`/data`, {
                    credentials: 'include'
                });
                
                if (!response.ok) {
                    throw new Error(`Eroare server: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.temperatura !== undefined && data.umiditate !== undefined) {
                    document.getElementById('temperature').textContent = `${data.temperatura}°C`;
                    document.getElementById('humidity').textContent = `${data.umiditate}%`;
                    document.getElementById('weather-status').textContent = 
                        data.umiditate > 70 ? 'Innorat si umed' : 
                        data.temperatura > 25 ? 'Insorit' : 'Normal';
                }
            } catch (error) {
                console.error('Eroare la actualizarea datelor:', error);
                alert('Eroare la comunicarea cu serverul');
            }
        });
    }
});