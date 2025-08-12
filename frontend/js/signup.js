document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const form = e.target;
    const data = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      password: form.password.value
    };

    // Client-side validation
    if (data.password.length < 6) {
      alert("Password must be at least 6 characters long.");
      return;
    }

    if (data.name.length < 2) {
      alert("Name must be at least 2 characters long.");
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
      alert("Please enter a valid email address.");
      return;
    }
  
    try {
      
      console.log('Attempting signup with:', { email: data.email });
      
      const response = await fetch("https://3.27.123.53.sslp.io/api/signup/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          
        },
        
        credentials: 'include',
        body: JSON.stringify(data)
      });
      
      console.log('Server response status:', response.status);
  
      const result = await response.json();
      console.log('Server response:', result);
      
      if (response.ok) {
        alert("Signup successful! Please login.");
        window.location.href = "index.html";
      } else {
        throw new Error(result.message || 'Signup failed');
      }
    } catch (error) {
      console.error('Signup error:', error);
      if (error.message.includes('Failed to fetch')) {
        alert('Unable to connect to server. Please check if the server is running.');
      } else {
        alert(`Signup failed: ${error.message}`);
      }
    }
});

// Real-time password validation
document.addEventListener("DOMContentLoaded", function() {
    const passwordInput = document.querySelector("input[name='password']");
    const passwordHint = document.querySelector(".password-hint");
    
    if (passwordInput && passwordHint) {
        passwordInput.addEventListener("input", function() {
            const password = this.value;
            
            if (password.length === 0) {
                passwordHint.textContent = "Password must be at least 6 characters long";
                passwordHint.className = "password-hint";
            } else if (password.length < 6) {
                passwordHint.textContent = `Password too short (${password.length}/6 characters)`;
                passwordHint.className = "password-hint error";
            } else {
                passwordHint.textContent = "Password length is good ✓";
                passwordHint.className = "password-hint success";
            }
        });
    }
});