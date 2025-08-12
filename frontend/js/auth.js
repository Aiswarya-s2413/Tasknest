// Authentication check function
function checkAuthentication() {
    fetch('/api/user/', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            // User not authenticated, redirect to login
            window.location.href = 'index.html';
        }
    })
    .catch(error => {
        console.error('Auth check failed:', error);
        // On error, redirect to login for safety
        window.location.href = 'index.html';
    });
}

// Logout function
function logout(event) {
    if (event) event.preventDefault();
    fetch('/api/logout/', {
        method: 'POST',
        credentials: 'include' 
    })
    .then(response => {
        // Always redirect to login after logout attempt
        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error('Error during logout:', error);
        // Even on error, redirect to login
        window.location.href = 'index.html';
    });
}