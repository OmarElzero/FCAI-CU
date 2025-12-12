# FCAI Student Activity Registration App - API Documentation

## Overview
The FCAI Student Activity Registration App is a Django REST API backend for managing student activities at the Faculty of Computing and Artificial Intelligence, Cairo University.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses Token Authentication. Include the token in the header:
```
Authorization: Token your-token-here
```

## User Roles
- **Super Admin**: Can create/manage admins, full system access
- **Admin**: Review activities, manage meetings, resolve conflicts
- **Student/Team**: Submit activities, make reservations

## API Endpoints

### Authentication Endpoints (`/api/auth/`)

#### Register User
- **POST** `/api/auth/register/`
- **Permission**: AllowAny
- **Body**:
```json
{
    "username": "string",
    "email": "string", 
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "password_confirm": "string",
    "role": "student|admin",
    "student_id": "string (optional for students)",
    "phone": "string (optional)"
}
```
- **Response**: User data + authentication token

#### Login
- **POST** `/api/auth/login/`
- **Permission**: AllowAny
- **Body**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response**: User data + authentication token

#### Logout
- **POST** `/api/auth/logout/`
- **Permission**: IsAuthenticated
- **Response**: Success message

#### Get Profile
- **GET** `/api/auth/profile/`
- **Permission**: IsAuthenticated
- **Response**: Current user profile data

#### Update Profile
- **PUT** `/api/auth/profile/`
- **Permission**: IsAuthenticated
- **Body**: Partial user data
- **Response**: Updated user profile

#### Change Password
- **POST** `/api/auth/change-password/`
- **Permission**: IsAuthenticated
- **Body**:
```json
{
    "old_password": "string",
    "new_password": "string", 
    "new_password_confirm": "string"
}
```

#### List Users (Super Admin Only)
- **GET** `/api/auth/list/`
- **Permission**: Super Admin only
- **Response**: List of all users

### Activity Endpoints (`/api/activities/`)

#### Submit Activity (Students)
- **POST** `/api/activities/submit/`
- **Permission**: Student only
- **Body** (multipart/form-data):
```json
{
    "team_name": "string",
    "team_description": "string",
    "logo": "file (optional)",
    "previous_contributions": "string",
    "expected_contribution": "string"
}
```
- **Response**: Success message + activity ID

#### Get My Activities (Students)
- **GET** `/api/activities/my-activities/`
- **Permission**: Student only
- **Response**: List of activities submitted by current student

#### List All Activities (Admin)
- **GET** `/api/activities/admin/list/`
- **Permission**: Admin/Super Admin
- **Query Parameters**: 
  - `status`: Filter by status (pending, approved, rejected, meeting_requested)
- **Response**: List of all activities

#### Activity Detail
- **GET** `/api/activities/{id}/`
- **Permission**: IsAuthenticated (students see own, admins see all)
- **Response**: Detailed activity information

#### Review Activity (Admin)
- **PUT** `/api/activities/admin/review/{id}/`
- **Permission**: Admin/Super Admin
- **Body**:
```json
{
    "status": "approved|rejected|meeting_requested",
    "admin_notes": "string (optional)"
}
```
- **Response**: Updated activity data
- **Note**: When approved, automatically adds to public timeline

#### Public Timeline
- **GET** `/api/activities/timeline/`
- **Permission**: AllowAny (Public)
- **Query Parameters**:
  - `limit`: Limit number of results
- **Response**: List of approved activities for public display

#### Activity Statistics (Admin)
- **GET** `/api/activities/admin/stats/`
- **Permission**: Admin/Super Admin
- **Response**: Activity statistics (total, pending, approved, etc.)

### Meeting Endpoints (`/api/meetings/`)

#### Request Meeting (Admin)
- **POST** `/api/meetings/admin/request/`
- **Permission**: Admin/Super Admin
- **Body**:
```json
{
    "activity": "activity_id",
    "student": "student_user_id",
    "admin_notes_before": "string (optional)",
    "time_slots": [
        {"proposed_datetime": "2025-01-15T10:00:00Z"},
        {"proposed_datetime": "2025-01-15T14:00:00Z"}
    ]
}
```
- **Response**: Meeting data
- **Note**: Updates activity status to "meeting_requested"

#### Student Meeting List
- **GET** `/api/meetings/student/list/`
- **Permission**: Student only
- **Response**: List of meetings for current student

#### Admin Meeting List  
- **GET** `/api/meetings/admin/list/`
- **Permission**: Admin/Super Admin
- **Response**: List of meetings (all for super admin, own for admin)

#### Meeting Detail
- **GET** `/api/meetings/{id}/`
- **Permission**: IsAuthenticated (students see own, admins see relevant)
- **Response**: Detailed meeting information

#### Select Time Slot (Student)
- **POST** `/api/meetings/student/select-slot/{meeting_id}/`
- **Permission**: Student only
- **Body**:
```json
{
    "time_slot_id": "integer",
    "student_notes": "string (optional)"
}
```
- **Response**: Updated meeting with Google Meet link
- **Note**: Changes status to "scheduled" and generates Meet link

#### Update Meeting Outcome (Admin)
- **POST** `/api/meetings/admin/outcome/{meeting_id}/`
- **Permission**: Admin/Super Admin
- **Body**:
```json
{
    "outcome": "approved|rejected|needs_revision",
    "admin_notes_after": "string"
}
```
- **Response**: Updated meeting data
- **Note**: Updates activity status based on outcome

#### Meeting Statistics (Admin)
- **GET** `/api/meetings/admin/stats/`
- **Permission**: Admin/Super Admin
- **Response**: Meeting statistics

### Reservation Endpoints (`/api/reservations/`)

#### List Locations
- **GET** `/api/reservations/locations/`
- **Permission**: AllowAny
- **Query Parameters**:
  - `type`: Filter by carnival or creativa availability
- **Response**: List of available locations

#### Check Available Slots
- **GET** `/api/reservations/available-slots/`
- **Permission**: AllowAny
- **Query Parameters**:
  - `date`: Required (YYYY-MM-DD)
  - `location`: Required (location ID)
  - `reservation_type`: Optional (regular, carnival, creativa)
- **Response**: Location info + existing reservations for the date

#### Create Reservation (Students)
- **POST** `/api/reservations/create/`
- **Permission**: Student only (for approved activities)
- **Body**:
```json
{
    "activity": "activity_id",
    "location": "location_id", 
    "start_datetime": "2025-01-15T10:00:00Z",
    "end_datetime": "2025-01-15T12:00:00Z",
    "reservation_type": "regular|carnival|creativa",
    "expected_attendees": "integer",
    "purpose": "string",
    "special_requirements": "string (optional)"
}
```
- **Response**: Success message + conflict information

#### My Reservations (Students)
- **GET** `/api/reservations/my-reservations/`
- **Permission**: Student only
- **Response**: List of reservations for current student's activities

#### Admin Reservation List
- **GET** `/api/reservations/admin/list/`
- **Permission**: Admin/Super Admin  
- **Query Parameters**:
  - `status`: Filter by status
  - `type`: Filter by reservation type
- **Response**: List of all reservations

#### Reservation Detail
- **GET** `/api/reservations/{id}/`
- **Permission**: IsAuthenticated (students see own, admins see all)
- **Response**: Detailed reservation with conflict information

#### Review Reservation (Admin)
- **PUT** `/api/reservations/admin/review/{id}/`
- **Permission**: Admin/Super Admin
- **Body**:
```json
{
    "status": "approved|rejected",
    "admin_notes": "string (optional)",
    "priority_score": "integer (optional)"
}
```
- **Response**: Updated reservation
- **Note**: Automatically resolves conflicts when approved

#### Get Reservation Conflicts (Admin)
- **GET** `/api/reservations/admin/conflicts/`
- **Permission**: Admin/Super Admin
- **Response**: List of pending reservation conflicts

#### Resolve Conflict (Admin)
- **POST** `/api/reservations/admin/resolve-conflict/{conflict_id}/`
- **Permission**: Admin/Super Admin
- **Body**:
```json
{
    "approved_reservation_id": "integer",
    "resolution_status": "resolved|escalated",
    "resolution_notes": "string"
}
```
- **Response**: Conflict resolution result

#### Reservation Statistics (Admin)
- **GET** `/api/reservations/admin/stats/`
- **Permission**: Admin/Super Admin
- **Response**: Reservation statistics

## Workflow Examples

### 1. Student Activity Submission & Approval
1. Student registers: `POST /api/auth/register/`
2. Student submits activity: `POST /api/activities/submit/`
3. Admin reviews: `PUT /api/activities/admin/review/{id}/` → status: "approved"
4. Activity appears on public timeline: `GET /api/activities/timeline/`

### 2. Meeting Request & Scheduling
1. Admin requests meeting: `POST /api/meetings/admin/request/`
2. Student selects time slot: `POST /api/meetings/student/select-slot/{id}/`
3. Meeting is scheduled with Google Meet link
4. After meeting, admin updates outcome: `POST /api/meetings/admin/outcome/{id}/`

### 3. Reservation with Conflict Resolution
1. Student creates reservation: `POST /api/reservations/create/`
2. System detects conflicts automatically
3. Admin reviews conflicts: `GET /api/reservations/admin/conflicts/`
4. Admin resolves conflict: `POST /api/reservations/admin/resolve-conflict/{id}/`

## Special Features

### Automatic Timeline Updates
- When activity is approved (directly or after meeting), it's automatically added to public timeline
- Timeline entry includes team info and announcement text

### Conflict Resolution Logic
- Priority-based: Higher priority score wins
- Time-based: Earlier submission wins if priority is equal
- Manual override: Admins can manually resolve conflicts

### Special Reservation Types
- **Thursday Carnival**: Special events on Thursdays
- **Creativa**: Creative/artistic events
- Locations can be configured for availability by type

## Error Responses
All endpoints return appropriate HTTP status codes:
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)  
- `404`: Not Found
- `500`: Internal Server Error

Error response format:
```json
{
    "error": "Error message",
    "details": "Additional details (optional)"
}
```

## Notes for Frontend Integration

### File Uploads
- Activity logo uploads use `multipart/form-data`
- Supported formats: JPG, PNG
- Images are automatically resized to 300x300px

### Authentication Flow
1. Login/Register to get token
2. Store token securely (localStorage/sessionStorage)
3. Include in Authorization header for all authenticated requests
4. Handle token expiry and refresh as needed

### Real-time Updates
- Consider implementing WebSocket connections for real-time notifications
- Poll timeline endpoint for public updates
- Admin dashboards may need frequent polling for new submissions

### Google Meet Integration
- Current implementation generates mock meet links
- Production should integrate with Google Calendar/Meet APIs
- Requires OAuth setup and API credentials