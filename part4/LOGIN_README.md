# HBnB Login Functionality

This document describes the implementation of the login functionality for the HBnB application.

## Files Created/Modified

### 1. `scripts.js` (New)
Contains the JavaScript code for handling login functionality:
- Event listener for login form submission
- AJAX request to login API endpoint
- JWT token storage in cookies
- Error handling and display
- Utility functions for cookie management

### 2. `login.html` (Modified)
Updated to include:
- Proper form ID (`login-form`)
- Script imports for `config.js` and `scripts.js`

### 3. `styles.css` (Modified)
Added error message styles:
- `.error-message` class for styling error notifications
- Fade-in animation for smooth error display

### 4. `config.js` (New)
Configuration file for API endpoints:
- Centralized API URL management
- Easy configuration for different environments

## How It Works

### Login Process

1. **Form Submission**: When user submits the login form, JavaScript prevents the default form submission
2. **Data Collection**: Email and password are extracted from form fields
3. **API Request**: AJAX request is made to the login endpoint with credentials
4. **Token Storage**: On successful login, JWT token is stored in a secure cookie
5. **Redirection**: User is redirected to the main page (`index.html`)
6. **Error Handling**: Failed logins display appropriate error messages

### Security Features

- **Secure Cookies**: JWT tokens are stored with `secure` and `samesite=strict` flags
- **Token Expiration**: Cookies have a 24-hour expiration (`max-age=86400`)
- **Input Validation**: HTML5 email validation and required fields
- **Error Messages**: Clear feedback for different error scenarios

## Configuration

### API Endpoint Setup

1. Open `config.js`
2. Update the `BASE_URL` with your actual API URL:
   ```javascript
   const API_CONFIG = {
       BASE_URL: 'https://your-actual-api-url.com',
       // ... rest of config
   };
   ```

### Expected API Response

The login endpoint should return a JSON response with the following structure on successful login:

```json
{
    "access_token": "your-jwt-token-here",
    "user": {
        "id": "user-id",
        "email": "user@example.com"
    }
}
```

## Error Handling

The implementation handles various error scenarios:

- **401 Unauthorized**: Invalid credentials
- **400 Bad Request**: Missing or invalid input
- **500 Server Error**: Server-side issues
- **Network Errors**: Connection problems

## Testing

### Manual Testing Steps

1. **Valid Login Test**:
   - Enter valid email and password
   - Verify successful login and redirection
   - Check that JWT token is stored in cookies

2. **Invalid Credentials Test**:
   - Enter invalid email/password
   - Verify error message is displayed
   - Ensure no token is stored

3. **Network Error Test**:
   - Disconnect from internet or use invalid API URL
   - Verify network error message is displayed

4. **Form validation Test**:
   - Try submitting empty form
   - Try submitting invalid email format
   - Verify HTML5 validation works

### Browser Console Testing

You can test the utility functions in the browser console:

```javascript
// Check if user is logged in
console.log(isLoggedIn());

// Get token value
console.log(getCookie('token'));
```

## Cookie Management

### Token Storage
- **Name**: `token`
- **Path**: `/` (available site-wide)
- **Max-Age**: 86400 seconds (24 hours)
- **Secure**: Yes (HTTPS only)
- **SameSite**: Strict

### Utility Functions
- `getCookie(name)`: Retrieve cookie value by name
- `isLoggedIn()`: Check if user has valid token

## Browser Compatibility

The implementation uses modern JavaScript features:
- `fetch()` API for AJAX requests
- `async/await` for asynchronous operations
- Modern DOM manipulation methods

Supported browsers:
- Chrome 42+
- Firefox 39+
- Safari 10.1+
- Edge 14+

## Future Enhancements

Potential improvements for production use:

1. **Token Refresh**: Implement automatic token renewal
2. **Remember Me**: Optional longer-term storage
3. **Session Management**: Track user sessions
4. **Two-Factor Authentication**: Additional security layer
5. **Social Login**: OAuth integration
6. **Password Recovery**: Forgot password functionality

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure API server allows requests from your domain
2. **Token Not Stored**: Check browser security settings and HTTPS usage
3. **Form Not Submitting**: Verify form ID and script loading order
4. **Styling Issues**: Ensure `styles.css` is loaded before scripts

### Debug Mode

To enable debug logging, add this to your browser console:
```javascript
// Enable detailed logging
window.DEBUG_LOGIN = true;
```
