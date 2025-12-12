# Authentication & Redirect Flow Documentation

## Overview
Fixed the authentication and redirect flow issues in the JobSearch application, particularly the infinite redirect loop between dashboard and login pages for admin users.

## Issues Fixed

### 1. **Infinite Redirect Loop**
- **Problem**: Admin users were getting stuck in a redirect loop between dashboard and login pages
- **Cause**: 
  - Missing redirect logic after successful login
  - Conflicting authentication checks between main.js and auth.js
  - Incorrect role checking (using `role === 'admin'` instead of `is_company`)

### 2. **Inconsistent Role Checking**
- **Problem**: Some files used `user.role === 'admin'` while others used `user.is_company`
- **Solution**: Standardized to use `user.is_company` throughout the application

### 3. **Missing Auto-login After Registration**
- **Problem**: After registration, users were not automatically logged in
- **Solution**: Implemented auto-login flow after successful registration

## Changes Made

### 1. **auth.js** - Main Authentication Module
```javascript
// Fixed login redirect logic
if (user.is_company) {
    window.location.href = basePath + 'features/admin/dashboard.html';
} else {
    window.location.href = basePath + 'features/user/search_jobs.html';
}

// Fixed signup auto-login
const loginResponse = await loginUserAPI(username, password);
// ... redirect based on user type
```

### 2. **main.js** - Removed Conflicting Auth Logic
- Removed duplicate authentication checks that conflicted with auth.js
- Fixed navbar visibility logic to use `user.is_company`
- Deprecated old auth functions in favor of auth.js module

### 3. **Body Classes** - Standardized Requirements
Updated all admin pages from `requires-admin` to `requires-company`:
- `dashboard.html`
- `add_job.html`
- `edit_job.html`
- `view_applicants.html`

### 4. **auth.check.js** - Enhanced Page Setup
- Fixed import path
- Added company name display for company users
- Improved UI element management

## Redirect Flow Logic

### **Login Flow**
1. User submits login form
2. API validates credentials
3. If successful:
   - Store user info in localStorage
   - Check for redirect parameter in URL
   - If redirect exists: go to original requested page
   - If no redirect:
     - Company users → `/features/admin/dashboard.html`
     - Regular users → `/features/user/search_jobs.html`

### **Registration Flow**
1. User submits registration form
2. API creates new user account
3. If successful:
   - Automatically login the user
   - Redirect based on user type:
     - Company users → `/features/admin/dashboard.html`
     - Regular users → `/features/user/search_jobs.html`

### **Page Access Control**
1. Protected pages run `auth.check.js` on load
2. `checkAuth()` function validates:
   - **requireAuth**: User must be logged in
   - **requireCompany**: User must have `is_company: true`
   - **requireJobSeeker**: User must have `is_company: false`
3. If requirements not met:
   - Redirect to login page (if not authenticated)
   - Redirect to appropriate user page (if wrong role)

### **Role-Based Redirects**
- **Company Users** trying to access job seeker pages → Dashboard
- **Job Seekers** trying to access company pages → Search Jobs
- **Unauthenticated** users trying to access protected pages → Login

## File Structure

### Authentication Files
- `assets/js/userjs/auth.js` - Main authentication logic
- `assets/js/userjs/auth.check.js` - Page protection middleware
- `assets/js/userjs/api.js` - API communication functions
- `assets/js/userjs/utils.js` - Utility functions

### Page Types
- **Public Pages**: `index.html`, `login.html`, `signup.html`
- **Company Pages**: All files in `features/admin/`
- **User Pages**: All files in `features/user/`
- **Mixed Access**: Some user pages accessible to all authenticated users

## Testing

Created `auth-test.html` for debugging authentication issues:
- Check current auth status
- View user information
- Test redirect flows
- Clear localStorage
- Debug API responses

## Best Practices Implemented

1. **Single Source of Truth**: All auth logic centralized in auth.js
2. **Consistent Role Checking**: Use `user.is_company` throughout
3. **Proper Error Handling**: Graceful fallbacks for failed API calls
4. **URL Preservation**: Redirect to originally requested page after login
5. **UI State Management**: Consistent body classes for styling
6. **Module System**: ES6 imports for better code organization

## Usage Instructions

### For Developers
1. Use `auth.check.js` on protected pages
2. Set appropriate body classes (`requires-auth`, `requires-company`)
3. Import auth functions from `userjs/auth.js`
4. Don't implement custom auth logic - use the centralized system

### For Testing
1. Open `auth-test.html` to debug auth issues
2. Check browser console for detailed error messages
3. Verify localStorage and session data
4. Test all redirect scenarios

## Error Prevention

- **Avoid Redirect Loops**: Check current page before redirecting
- **Handle API Failures**: Graceful degradation when backend is unavailable
- **Validate User Data**: Proper null/undefined checks
- **Consistent State**: Sync localStorage with server session
