# JobSearch API Documentation

## User Endpoints

### Register
- **URL:** `/api/users/register/`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "is_company": false,
    "company": "string or null"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "is_company": false,
    "company": "string or null",
    "created_at": "2025-05-17T12:00:00Z"
  }
  ```

---

### Login
- **URL:** `/api/users/login/`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "is_company": false,
    "company": "string or null",
    "created_at": "2025-05-17T12:00:00Z"
  }
  ```
  - On error: `{ "error": "Invalid credentials" }`

---

### Logout
- **URL:** `/api/users/logout/`
- **Method:** POST
- **Headers:** (must be authenticated)
- **Response:**
  ```json
  { "success": "Logged out" }
  ```

---

### List Users (admin only)
- **URL:** `/api/users/`
- **Method:** GET
- **Headers:** (must be authenticated as admin)
- **Response:** List of user objects

---

## Job Endpoints

### List Jobs
- **URL:** `/api/jobs/`
- **Method:** GET
- **Query Params:** `company=string` (optional), `status=Open|Closed` (optional)
- **Response:** List of job objects

---

### Create Job (company/admin only)
- **URL:** `/api/jobs/`
- **Method:** POST
- **Headers:** (must be authenticated as company/admin)
- **Request Body:**
  ```json
  {
    "title": "string",
    "salary": "string",
    "company": "string",
    "status": "Open",
    "experience": 2,
    "description": "string"
  }
  ```
- **Response:** Job object

---

### Retrieve/Update/Delete Job
- **URL:** `/api/jobs/{id}/`
- **Method:** GET, PUT, PATCH, DELETE
- **Headers:** (update/delete: must be authenticated as creator)
- **Response:** Job object (GET/PUT/PATCH), 204 No Content (DELETE)

---

## Application Endpoints

### List Applications
- **URL:** `/api/applications/`
- **Method:** GET
- **Headers:** (must be authenticated)
- **Response:**
  - If user: applications submitted by user
  - If company: applications for jobs at user's company

---

### Create Application (user only)
- **URL:** `/api/applications/`
- **Method:** POST
- **Headers:** (must be authenticated as user)
- **Request Body:**
  ```json
  {
    "job": 1,
    "status": "pending" // optional, defaults to "pending"
  }
  ```
- **Response:** Application object

---

### Retrieve/Update/Delete Application
- **URL:** `/api/applications/{id}/`
- **Method:** GET, PUT, PATCH, DELETE
- **Headers:** (must be authenticated, only owner/company can update/delete)
- **Response:** Application object (GET/PUT/PATCH), 204 No Content (DELETE)

---

## Notes
- All endpoints except register/login require authentication (session or token).
- For company/admin, set `"is_company": true` on registration.
- Use the `/api/` prefix for all endpoints.
- You can use session authentication (login endpoint) or add token authentication if needed.
