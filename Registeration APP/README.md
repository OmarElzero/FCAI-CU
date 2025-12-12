# FCAI Student Activity Registration App

A Django REST API backend for managing student activities at the Faculty of Computing and Artificial Intelligence (FCAI), Cairo University.

## Features

### 🔐 Authentication & User Management
- Role-based authentication (Super Admin, Admin, Student)
- Token-based API authentication
- User registration and profile management

### 📋 Activity Management
- Student activity submission with file upload support
- Admin review system (approve/reject/request meeting)
- Automatic public timeline updates
- Activity statistics and reporting

### 🤝 Meeting System
- Admin-initiated meeting requests
- Time slot selection by students
- Google Meet integration (simplified)
- Meeting outcome tracking

### 📍 Reservation System
- Location and time slot reservations
- Conflict detection and resolution
- Special event types (Thursday Carnival, Creativa)
- Priority-based conflict resolution

### 📊 Admin Dashboard APIs
- Comprehensive statistics
- Conflict management
- Activity and reservation oversight

## Quick Start

### 1. Installation
```bash
# Clone and navigate to project
cd "FCAI-CU/Registeration APP"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Or create via shell:
echo "from users.models import User; User.objects.create_superuser('admin', 'admin@fcai.cu.edu.eg', 'admin123', role='super_admin')" | python manage.py shell

# Create sample locations
python manage.py create_sample_locations
```

### 3. Run Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Documentation

Complete API documentation is available in [`API_Documentation.md`](./API_Documentation.md).

### Key Endpoints:
- **Authentication**: `/api/auth/`
- **Activities**: `/api/activities/`
- **Meetings**: `/api/meetings/`
- **Reservations**: `/api/reservations/`

### Admin Interface:
Access the Django admin at `http://localhost:8000/admin/`

## Testing

### Automated Testing
```bash
python test_api.py
```

### Manual Testing
1. Use the provided API documentation
2. Test with tools like Postman or curl
3. Check the Django admin interface

## Project Structure

```
FCAI Registration App/
├── fcai_registration_app/     # Main Django project
├── users/                     # User management app
├── activities/               # Activity management app
├── meetings/                # Meeting system app
├── reservations/            # Reservation system app
├── media/                   # Uploaded files (logos)
├── API_Documentation.md     # Complete API docs
├── test_api.py             # API testing script
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## Key Models

### User Model
- Custom user with roles (super_admin, admin, student)
- Student ID field for students
- Contact information

### Activity Model
- Team information and descriptions
- Logo upload support
- Review status and admin notes
- Timeline integration

### Meeting Model
- Admin-student meeting management
- Time slot proposals and selection
- Google Meet integration
- Outcome tracking

### Reservation Model
- Location and time booking
- Conflict detection
- Special event type support
- Priority-based resolution

### Location Model
- Available spaces for activities
- Capacity and facilities info
- Event type availability flags

## Workflow Examples

### 1. Student Activity Submission
```
Student → Submit Activity → Admin Review → Approval → Public Timeline
```

### 2. Meeting Scheduling
```
Admin → Request Meeting → Student Selects Time → Auto Meet Link → Meeting Outcome
```

### 3. Reservation with Conflicts
```
Student → Create Reservation → Conflict Detection → Admin Resolution → Final Status
```

## Important Features

### ✨ Timeline Auto-Update
- When activities are approved, they automatically appear on the public timeline
- No manual intervention needed

### ⚡ Conflict Resolution  
- Automatic conflict detection for overlapping reservations
- Priority-based resolution system
- Manual override capabilities for admins

### 🎯 Special Event Support
- Thursday Carnival events
- Creativa artistic events  
- Location-based availability settings

### 📱 API-First Design
- Complete REST API for frontend integration
- Token-based authentication
- Comprehensive error handling

## Production Considerations

### Security
- Change `SECRET_KEY` in production
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use environment variables for sensitive settings

### Database
- Configure PostgreSQL/MySQL for production
- Set up proper backup strategies
- Consider database indexing for performance

### File Storage
- Configure cloud storage (AWS S3, etc.) for media files
- Set up CDN for static files

### Google Meet Integration
- Implement proper Google Calendar/Meet API integration
- Set up OAuth credentials
- Handle API rate limits

### Monitoring
- Add logging configuration
- Set up error tracking (Sentry, etc.)
- Monitor API performance

## Support

For questions or issues:
1. Check the API documentation
2. Review the Django admin interface
3. Test with the provided testing script
4. Examine the codebase for implementation details

## License

This project is developed for the Faculty of Computing and Artificial Intelligence, Cairo University.

---

**Next Steps for Frontend Integration:**
1. Use the comprehensive API documentation
2. Implement authentication flow with token storage
3. Build user interfaces for each role (student, admin, super admin)
4. Handle file uploads for activity logos
5. Implement real-time updates for timeline and notifications