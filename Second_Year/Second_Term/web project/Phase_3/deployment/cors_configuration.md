# Configuring CORS in Django for Frontend-Backend Integration

This guide explains how to configure CORS (Cross-Origin Resource Sharing) in your Django backend to allow requests from your frontend application.

## What is CORS?

CORS is a security feature implemented by browsers that blocks web pages from making requests to a different domain than the one that served the web page. Without proper CORS configuration, your frontend won't be able to communicate with your backend API if they're hosted on different domains or ports.

## Step 1: Ensure django-cors-headers is Installed

Check your requirements.txt file to confirm that django-cors-headers is included:

```
django-cors-headers==4.7.0  # Already in your requirements
```

If it's not installed, you can install it with:

```bash
pip install django-cors-headers
```

## Step 2: Configure CORS in Django Settings

Update your Django settings.py file to include the necessary CORS configuration:

```python
# In jobsearch/settings.py

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",    # Development server
    "http://127.0.0.1:8000",    # Alternative development server
    "http://localhost:5500",    # Live Server extension in VSCode
    "http://127.0.0.1:5500",    # Alternative Live Server
    # Add your production domains here
    # "https://yourdomain.com",
]

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# If you need to allow all headers
CORS_ALLOW_ALL_HEADERS = True

# Alternatively, specify which headers are allowed
# CORS_ALLOW_HEADERS = [
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
# ]
```

## Step 3: Update MIDDLEWARE Setting

Make sure the CORS middleware is correctly positioned in your MIDDLEWARE setting:

```python
# In jobsearch/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware (should be before CommonMiddleware)
    'django.middleware.common.CommonMiddleware',
    # ... other middleware ...
]
```

## Step 4: Configure CSRF Protection

For production with HTTPS, you might need to configure CSRF settings:

```python
# In jobsearch/settings.py

# For production with HTTPS
CSRF_COOKIE_SECURE = True  # Only send the cookie over HTTPS
SESSION_COOKIE_SECURE = True  # Only send the session cookie over HTTPS
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the CSRF cookie
CSRF_USE_SESSIONS = True  # Store CSRF token in the session instead of a cookie
CSRF_TRUSTED_ORIGINS = [
    "https://yourdomain.com",  # Add your production domains here
]
```

## Step 5: Testing CORS Configuration

After updating your settings, test your CORS configuration:

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Open your frontend application and make an API request to your backend.

3. Check the browser's developer console for any CORS-related errors.

## Step 6: Production Considerations

When deploying to production:

1. Remove development URLs from CORS_ALLOWED_ORIGINS
   
2. Add your production domain(s) to CORS_ALLOWED_ORIGINS

3. Use HTTPS for all communications between frontend and backend

4. Consider implementing more restrictive CORS policies if needed

## Troubleshooting CORS Issues

If you encounter CORS issues:

1. Check the browser's developer console for specific error messages

2. Verify that your frontend's origin matches exactly what's in CORS_ALLOWED_ORIGINS (including http/https, subdomains, and ports)

3. Ensure the CORS middleware is positioned correctly in the middleware list

4. For complex requests (non-GET), check that preflight OPTIONS requests are being handled correctly

5. Make sure cookies and credentials are properly configured on both sides

## Example API Request with Credentials

When making API requests from the frontend, ensure you include the credentials:

```javascript
fetch('http://localhost:8000/api/users/current/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'include', // Important for sending cookies
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

By following this guide, you should have a properly configured CORS setup that allows your frontend and backend to communicate securely.
