#!/usr/bin/env python3
"""
FCAI Registration App - API Testing Script

This script demonstrates the main API functionality.
Run the Django server first: python manage.py runserver
Then run this script: python test_api.py
"""

import requests
import json
from datetime import datetime, timedelta
import os

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.tokens = {}
        
    def register_and_login(self, username, email, password, role='student', student_id=None):
        """Register a new user and return their token"""
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password,
            'role': role,
            'first_name': username.title(),
            'last_name': 'Test',
        }
        if student_id:
            data['student_id'] = student_id
            
        # Register
        response = self.session.post(f"{BASE_URL}/auth/register/", json=data)
        if response.status_code == 201:
            result = response.json()
            token = result['token']
            self.tokens[username] = token
            print(f"✓ {username} registered successfully (Role: {role})")
            return token
        else:
            # Try login if user already exists
            login_data = {'username': username, 'password': password}
            response = self.session.post(f"{BASE_URL}/auth/login/", json=login_data)
            if response.status_code == 200:
                result = response.json()
                token = result['token']
                self.tokens[username] = token
                print(f"✓ {username} logged in successfully (Role: {role})")
                return token
            else:
                print(f"✗ Failed to register/login {username}: {response.text}")
                return None
    
    def make_request(self, method, endpoint, username=None, **kwargs):
        """Make authenticated API request"""
        headers = {}
        if username and username in self.tokens:
            headers['Authorization'] = f"Token {self.tokens[username]}"
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        url = f"{BASE_URL}{endpoint}"
        response = getattr(self.session, method.lower())(url, **kwargs)
        return response
    
    def test_activity_workflow(self):
        """Test complete activity workflow"""
        print("\n=== Testing Activity Workflow ===")
        
        # 1. Student submits activity
        activity_data = {
            'team_name': 'AI Innovation Club',
            'team_description': 'A club focused on AI research and innovation projects',
            'previous_contributions': 'Organized 3 workshops on machine learning',
            'expected_contribution': 'Plan to host AI conference and mentor students'
        }
        
        response = self.make_request('post', '/activities/submit/', 'student1', json=activity_data)
        if response.status_code == 201:
            activity_id = response.json().get('activity_id')
            print(f"✓ Activity submitted successfully (ID: {activity_id})")
        else:
            print(f"✗ Activity submission failed: {response.text}")
            return None
        
        # 2. Admin reviews activity
        review_data = {
            'status': 'approved',
            'admin_notes': 'Great initiative! Approved for implementation.'
        }
        
        response = self.make_request('put', f'/activities/admin/review/{activity_id}/', 'admin1', json=review_data)
        if response.status_code == 200:
            print("✓ Activity approved by admin")
        else:
            print(f"✗ Activity review failed: {response.text}")
        
        # 3. Check public timeline
        response = self.make_request('get', '/activities/timeline/')
        if response.status_code == 200:
            timeline = response.json()
            print(f"✓ Public timeline updated - {timeline['count']} activities visible")
        else:
            print(f"✗ Timeline fetch failed: {response.text}")
        
        return activity_id
    
    def test_meeting_workflow(self, activity_id):
        """Test meeting request and scheduling"""
        print("\n=== Testing Meeting Workflow ===")
        
        if not activity_id:
            print("✗ No activity ID provided, skipping meeting test")
            return
        
        # 1. Admin requests meeting
        meeting_data = {
            'activity': activity_id,
            'student': 2,  # Assuming student1 has ID 2
            'admin_notes_before': 'Would like to discuss implementation timeline',
            'time_slots': [
                {'proposed_datetime': (datetime.now() + timedelta(days=1)).isoformat() + 'Z'},
                {'proposed_datetime': (datetime.now() + timedelta(days=2)).isoformat() + 'Z'}
            ]
        }
        
        response = self.make_request('post', '/meetings/admin/request/', 'admin1', json=meeting_data)
        if response.status_code == 201:
            meeting_id = response.json().get('meeting_id')
            print(f"✓ Meeting requested successfully (ID: {meeting_id})")
        else:
            print(f"✗ Meeting request failed: {response.text}")
            return
        
        # 2. Student selects time slot (assuming first slot ID is 1)
        slot_data = {
            'time_slot_id': 1,
            'student_notes': 'Available for the proposed time, looking forward to the meeting'
        }
        
        response = self.make_request('post', f'/meetings/student/select-slot/{meeting_id}/', 'student1', json=slot_data)
        if response.status_code == 200:
            meeting_info = response.json()
            print(f"✓ Time slot selected - Meet link generated")
        else:
            print(f"✗ Time slot selection failed: {response.text}")
    
    def test_reservation_workflow(self, activity_id):
        """Test reservation system with conflict detection"""
        print("\n=== Testing Reservation Workflow ===")
        
        if not activity_id:
            print("✗ No activity ID provided, skipping reservation test")
            return
        
        # 1. Check available locations
        response = self.make_request('get', '/reservations/locations/')
        if response.status_code == 200:
            locations = response.json()
            if locations:
                location_id = locations[0]['id']
                print(f"✓ Found {len(locations)} available locations")
            else:
                print("✗ No locations available")
                return
        else:
            print(f"✗ Location fetch failed: {response.text}")
            return
        
        # 2. Create reservation
        tomorrow = datetime.now().date() + timedelta(days=1)
        reservation_data = {
            'activity': activity_id,
            'location': location_id,
            'start_datetime': f"{tomorrow}T10:00:00Z",
            'end_datetime': f"{tomorrow}T12:00:00Z",
            'reservation_type': 'regular',
            'expected_attendees': 50,
            'purpose': 'AI Workshop for students',
            'special_requirements': 'Projector and microphone needed'
        }
        
        response = self.make_request('post', '/reservations/create/', 'student1', json=reservation_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Reservation created successfully")
            if result.get('has_conflicts'):
                print(f"⚠ Conflicts detected: {result.get('conflicts_count')} conflicts")
        else:
            print(f"✗ Reservation creation failed: {response.text}")
    
    def test_admin_stats(self):
        """Test admin statistics endpoints"""
        print("\n=== Testing Admin Statistics ===")
        
        endpoints = [
            '/activities/admin/stats/',
            '/meetings/admin/stats/', 
            '/reservations/admin/stats/'
        ]
        
        for endpoint in endpoints:
            response = self.make_request('get', endpoint, 'admin1')
            if response.status_code == 200:
                stats = response.json()
                print(f"✓ {endpoint}: {len(stats)} metrics available")
            else:
                print(f"✗ {endpoint}: Failed to fetch stats")
    
    def run_full_test(self):
        """Run complete API test suite"""
        print("🚀 Starting FCAI Registration App API Tests")
        print("=" * 50)
        
        # Setup test users
        self.register_and_login('admin1', 'admin1@fcai.cu.edu.eg', 'admin123', 'admin')
        self.register_and_login('student1', 'student1@fcai.cu.edu.eg', 'student123', 'student', '20210001')
        
        # Run workflow tests
        activity_id = self.test_activity_workflow()
        self.test_meeting_workflow(activity_id)
        self.test_reservation_workflow(activity_id)
        self.test_admin_stats()
        
        print("\n" + "=" * 50)
        print("🎉 API Testing Complete!")
        print("\nNext steps:")
        print("1. Check Django admin at http://localhost:8000/admin/")
        print("2. View API documentation in API_Documentation.md")
        print("3. Test endpoints manually with Postman/curl")

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure Django server is running: python manage.py runserver")
    input("Press Enter when server is ready...")
    
    tester = APITester()
    tester.run_full_test()