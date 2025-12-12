# Project: FCAI Cairo University Student Activity Registration App

## Purpose:
A web-based platform to manage student activities for the Faculty of Computing and Artificial Intelligence (FCAI), Cairo University.

## Tech Stack (Backend Only)

**Framework:** Django (Python).

**Focus:** Only backend development (APIs, authentication, business logic, database models).

**Frontend:** Out of scope (to be developed later by another team or through API integration).

## User Roles

### Super Admin
- Create and manage Admins.

### Admin
- Reviews and approves/rejects student activity requests.
- Can request meetings with applicant teams.
- Resolves conflicts between activities.

### Student / Team
- Can request to register a new student activity.
- Can reserve slots/locations for approved activities.

## Backend Workflow

### 1. Public Timeline
API to fetch and display the timeline of current activities (public access).

### 2. Activity Registration
Endpoint to submit a student activity request with:
- Team logo (file upload).
- Team name.
- Team description.
- Previous contributions.
- Expected contribution to the faculty.

Stored in the database and flagged as Pending for Admin review.

### 3. Admin Review
Endpoints for Admin actions:
- **Approve** → Mark activity as official.
- **Reject** → Close request.
- **Request Meeting** →
  - Store available times.
  - Allow student team to select a slot.
  - Integration with Google Meet API to generate meeting link.
  - After meeting → Admin updates status (Approved/Rejected).

### 4. Activity Privileges
Once approved:
- APIs allow the team to request slot/location reservations.
- Filtering endpoints: by date and time.
- Special flag for Thursday Carnival reservations.
- Special flag for Creativa reservations.

### 5. Reservation Workflow
- Reservation requests are submitted via API.
- Admin can:
  - Approve.
  - Reject.
- If conflicts exist → Admin resolves based on team contribution & needs (custom logic defined in backend).

## Backend Key Features (MVP Scope)
- Django models for Users, Roles, Activities, Reservations, Meetings.
- Role-based authentication (Super Admin, Admin, Student).
- File upload handling for logos.
- Google Meet integration.
- Conflict resolution logic for reservations.
- RESTful APIs for frontend consumption.
