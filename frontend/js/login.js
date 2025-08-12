const API_BASE = "http://3.27.123.53/api"; 

// Utility functions for showing messages
function showError(elementId, message) {
  const errorElement = document.getElementById(elementId);
  errorElement.textContent = message;
  errorElement.classList.remove("hidden");
}

function hideError(elementId) {
  const errorElement = document.getElementById(elementId);
  errorElement.classList.add("hidden");
}

function showSuccess(elementId, message) {
  const successElement = document.getElementById(elementId);
  successElement.textContent = message;
  successElement.classList.remove("hidden");
}

function hideSuccess(elementId) {
  const successElement = document.getElementById(elementId);
  successElement.classList.add("hidden");
}

// Switch tabs
document.getElementById("password-tab").addEventListener("click", () => {
  // Update tab buttons
  document.getElementById("password-tab").classList.add("active");
  document.getElementById("otp-tab").classList.remove("active");
  
  // Switch forms
  document.getElementById("login-form").classList.remove("hidden");
  document.getElementById("otp-form").classList.add("hidden");
  
  // Clear any error messages
  hideError("login-error");
  hideError("otp-error");
  hideSuccess("otp-success");
});

document.getElementById("otp-tab").addEventListener("click", () => {
  // Update tab buttons
  document.getElementById("otp-tab").classList.add("active");
  document.getElementById("password-tab").classList.remove("active");
  
  // Switch forms
  document.getElementById("login-form").classList.add("hidden");
  document.getElementById("otp-form").classList.remove("hidden");
  
  // Clear any error messages
  hideError("login-error");
  hideError("otp-error");
  hideSuccess("otp-success");
});

// Password login
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  // Clear any previous error messages
  hideError("login-error");
  
  const email = e.target.email.value;
  const password = e.target.password.value;

  try {
    const res = await fetch(`${API_BASE}/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
      credentials: "include"
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.message || "Invalid email or password. Please try again.");
    }

    const data = await res.json();
    // Redirect to dashboard on successful login
    window.location.href = "dashboard.html";
  } catch (err) {
    // Show error message inline
    if (err.message.includes('Failed to fetch')) {
      showError("login-error", "Unable to connect to server. Please check your connection and try again.");
    } else {
      showError("login-error", err.message);
    }
  }
});

// OTP login - Request OTP
document.getElementById("request-otp").addEventListener("click", async () => {
  // Clear any previous messages
  hideError("otp-error");
  hideSuccess("otp-success");
  
  const email = document.querySelector("input[name='otp-email']").value;

  if (!email) {
    showError("otp-error", "Please enter your email address.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/request-otp/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.message || "Failed to send OTP");
    }

    showSuccess("otp-success", "OTP sent to your email! Please check your inbox.");
    document.getElementById("otp-input-group").classList.remove("hidden");
    document.getElementById("verify-otp").classList.remove("hidden");
  } catch (err) {
    if (err.message.includes('Failed to fetch')) {
      showError("otp-error", "Unable to connect to server. Please check your connection and try again.");
    } else {
      showError("otp-error", err.message);
    }
  }
});

// OTP login - Verify OTP
document.getElementById("verify-otp").addEventListener("click", async () => {
  // Clear any previous messages
  hideError("otp-error");
  hideSuccess("otp-success");
  
  const email = document.querySelector("input[name='otp-email']").value;
  const otp = document.querySelector("input[name='otp-code']").value;

  if (!otp) {
    showError("otp-error", "Please enter the OTP code.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/verify-otp/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, otp }),
      credentials: "include"
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.message || "Invalid OTP. Please try again.");
    }

    // Redirect to dashboard on successful login
    window.location.href = "dashboard.html";
  } catch (err) {
    if (err.message.includes('Failed to fetch')) {
      showError("otp-error", "Unable to connect to server. Please check your connection and try again.");
    } else {
      showError("otp-error", err.message);
    }
  }
});
