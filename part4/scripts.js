// Login functionality for HBnB application
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form data
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Clear any existing error messages
            clearErrorMessage();
            
            try {
                await loginUser(email, password);
            } catch (error) {
                console.error('Login error:', error);
                displayErrorMessage('An unexpected error occurred. Please try again.');
            }
        });
    }
});

/**
 * Handles user login by making API request
 * @param {string} email - User's email
 * @param {string} password - User's password
 */
async function loginUser(email, password) {
    try {
        // Use API configuration
        const apiUrl = typeof API_CONFIG !== 'undefined' ? 
            `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.LOGIN}` : 
            'https://your-api-url/login';
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            
            // Store JWT token in cookie
            document.cookie = `token=${data.access_token}; path=/; max-age=86400; secure; samesite=strict`;
            
            // Redirect to main page
            window.location.href = 'index.html';
        } else {
            // Handle different error status codes
            let errorMessage = 'Login failed. Please check your credentials.';
            
            if (response.status === 401) {
                errorMessage = 'Invalid email or password.';
            } else if (response.status === 400) {
                errorMessage = 'Please provide valid email and password.';
            } else if (response.status === 500) {
                errorMessage = 'Server error. Please try again later.';
            }
            
            displayErrorMessage(errorMessage);
        }
    } catch (error) {
        console.error('Network error:', error);
        displayErrorMessage('Network error. Please check your connection and try again.');
    }
}

/**
 * Displays error message to the user
 * @param {string} message - Error message to display
 */
function displayErrorMessage(message) {
    // Remove any existing error message
    clearErrorMessage();
    
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.id = 'error-message';
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    // Insert error message before the form
    const loginForm = document.getElementById('login-form');
    loginForm.parentNode.insertBefore(errorDiv, loginForm);
}

/**
 * Clears any existing error messages
 */
function clearErrorMessage() {
    const existingError = document.getElementById('error-message');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Utility function to get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} - Cookie value or null if not found
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Utility function to check if user is logged in
 * @returns {boolean} - True if user has valid token
 */
function isLoggedIn() {
    return getCookie('token') !== null;
}
