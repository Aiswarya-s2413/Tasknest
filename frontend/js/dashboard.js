function logout(event) {
    if (event) event.preventDefault();
    fetch('http://3.27.123.53/api/logout/', {
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
