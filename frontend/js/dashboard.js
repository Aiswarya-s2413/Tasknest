function logout(event) {
    if (event) event.preventDefault();
    fetch('http://127.0.0.1:8000/api/logout/', {
        method: 'POST',
        credentials: 'include' 
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '../index.html';
        } else {
            console.error('Logout failed');
        }
    })
    .catch(error => {
        console.error('Error during logout:', error);
    });
}
