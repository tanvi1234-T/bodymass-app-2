# Security Documentation

## Overview
This document outlines the security measures implemented in the Body Mass Index (BMI) Calculator web application. The app uses Streamlit for the frontend and Python for backend logic, with a focus on secure user authentication and data handling.

## Authentication System

### User Registration and Login
- **User Storage**: User credentials are stored in a JSON file (`users.json`) locally on the server.
- **Password Hashing**: Passwords are hashed using SHA256 before storage to prevent plaintext exposure.
- **Authentication Flow**: Users must log in to access the BMI calculator. Invalid credentials are rejected with appropriate error messages.

### Password Requirements
Passwords must meet the following criteria for security:
- Length: Between 13 and 27 characters
- Complexity: Must include at least one uppercase letter, one lowercase letter, and one special character
- Forbidden Characters: Passwords cannot contain the following characters: `=<>"'`
- No consecutive identical characters allowed

### Input Validation
- **Sanitization**: All user inputs are validated to prevent injection attacks and ensure data integrity.
- **Forbidden Characters**: Inputs are checked for dangerous characters that could be used in attacks.
- **Error Handling**: Invalid inputs are rejected with user-friendly error messages without revealing system details.

## Data Protection
- **Local Storage**: User data is stored locally in JSON format. In a production environment, consider migrating to a secure database.
- **No Sensitive Data Exposure**: The app does not store or transmit sensitive personal information beyond usernames and hashed passwords.
- **Session Management**: Streamlit handles session state, but no additional session security measures are implemented beyond basic authentication.

## Security Best Practices
- **HTTPS**: Ensure the application is served over HTTPS in production to encrypt data in transit.
- **Regular Updates**: Keep dependencies (Streamlit, Python libraries) updated to patch known vulnerabilities.
- **Access Control**: Only authenticated users can access the BMI calculation features.
- **Logging**: Consider implementing logging for authentication attempts to monitor for suspicious activity.

## Known Limitations
- **Local JSON Storage**: Not suitable for multi-user or production environments due to lack of concurrency control and security.
- **No Rate Limiting**: No protection against brute-force attacks on login.
- **Client-Side Security**: As a web app, client-side code is exposed; sensitive logic should be server-side.

## Recommendations
- Implement proper database storage (e.g., PostgreSQL with SQLAlchemy).
- Add rate limiting and CAPTCHA for authentication endpoints.
- Use environment variables for configuration instead of hardcoded values.
- Conduct regular security audits and penetration testing.

## Contact
For security concerns or questions, please contact the development team.