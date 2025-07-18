# 🔐 Security Guide

## Authentication System

The Carbon Emissions Calculator includes a simple but secure authentication system with the following features:

### 🔒 Security Features

1. **Password Hashing**: All passwords are hashed using SHA-256 with a salt
2. **Session Management**: User sessions are managed securely through Streamlit's session state
3. **Input Validation**: All user inputs are validated before processing
4. **Data Isolation**: Each user only has access to their own data
5. **Secure Storage**: User data is stored locally with proper file permissions

### 👤 User Management

- **Registration**: Users can create accounts with username, password, and optional email
- **Authentication**: Secure login with credential validation
- **Profile Management**: Users can update their settings and view account information
- **Data Reset**: Users can reset their emission data if needed

### 🚀 Demo Accounts

- **Quick Start**: Users can create temporary demo accounts for testing
- **Auto-cleanup**: Demo accounts older than 24 hours are automatically removed
- **Full Features**: Demo accounts have access to all calculator features

### 👑 Admin Features

- **User Statistics**: View total users, active users, and demo accounts
- **User Management**: Monitor user accounts and activity
- **Demo Cleanup**: Remove old demo accounts
- **Data Export**: Export anonymized user statistics

## 🔐 Admin Access

To access the admin panel:

1. Navigate to `/admin/admin_panel.py` in the app
2. Login with admin credentials:
   - Username: `admin`
   - Password: `admin123`

**⚠️ Important**: Change the default admin credentials in production!

## 🛡️ Security Best Practices

### For Production Deployment:

1. **Change Admin Credentials**: Update `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `admin/admin_panel.py`
2. **Environment Variables**: Store sensitive data in environment variables
3. **HTTPS**: Use HTTPS in production
4. **Database**: Consider using a proper database instead of JSON files
5. **Session Security**: Implement session timeout and secure session handling
6. **Input Sanitization**: Additional input validation for production use

### Current Limitations:

- Simple file-based storage (suitable for development/small deployments)
- Basic password hashing (consider bcrypt for production)
- No email verification
- No password reset functionality
- No rate limiting for login attempts

## 🔄 Migration to Production Database

For production use, consider migrating to:
- PostgreSQL or MySQL for user data
- Redis for session management
- OAuth2 for third-party authentication
- JWT tokens for stateless authentication

## 📝 Privacy

- User passwords are never stored in plaintext
- Only hashed passwords are saved
- User data is isolated per account
- No sensitive information is logged
- Demo accounts are automatically cleaned up
