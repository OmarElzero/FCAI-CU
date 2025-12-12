#!/bin/bash

echo "🧪 Setting up test data for frontend testing..."

API_BASE="http://localhost:8000/api"

# Create a test regular user
echo "1. Creating test regular user..."
REGULAR_USER_RESPONSE=$(curl -s -X POST "$API_BASE/users/register/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "frontend_test_user",
        "email": "user@frontend.test",
        "password": "testpass123",
        "is_company": false
    }')
echo "Regular user created: $REGULAR_USER_RESPONSE"

# Create a test company user
echo "2. Creating test company user..."
COMPANY_USER_RESPONSE=$(curl -s -X POST "$API_BASE/users/register/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "frontend_test_company",
        "email": "company@frontend.test",
        "password": "testpass123",
        "is_company": true,
        "company": "Frontend Test Corp"
    }')
echo "Company user created: $COMPANY_USER_RESPONSE"

# Login as company user to create jobs
echo "3. Logging in as company user..."
curl -s -X POST "$API_BASE/users/login/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "frontend_test_company",
        "password": "testpass123"
    }' \
    -c company_cookies.txt > /dev/null

# Create test jobs
echo "4. Creating test jobs..."

# Job 1
JOB1_RESPONSE=$(curl -s -X POST "$API_BASE/jobs/" \
    -H "Content-Type: application/json" \
    -b company_cookies.txt \
    -d '{
        "title": "Frontend Developer",
        "salary": "65000",
        "company": "Frontend Test Corp",
        "status": "Open",
        "experience": 2,
        "description": "We are looking for a skilled Frontend Developer to join our team. Experience with React, Vue, or Angular required."
    }')
echo "Job 1 created: $JOB1_RESPONSE"

# Job 2
JOB2_RESPONSE=$(curl -s -X POST "$API_BASE/jobs/" \
    -H "Content-Type: application/json" \
    -b company_cookies.txt \
    -d '{
        "title": "Backend Developer",
        "salary": "70000",
        "company": "Frontend Test Corp",
        "status": "Open",
        "experience": 3,
        "description": "Looking for an experienced Backend Developer with Python/Django expertise. Must have experience with APIs and databases."
    }')
echo "Job 2 created: $JOB2_RESPONSE"

# Job 3
JOB3_RESPONSE=$(curl -s -X POST "$API_BASE/jobs/" \
    -H "Content-Type: application/json" \
    -b company_cookies.txt \
    -d '{
        "title": "Full Stack Developer",
        "salary": "80000",
        "company": "Frontend Test Corp",
        "status": "Open",
        "experience": 4,
        "description": "Seeking a Full Stack Developer with experience in both frontend and backend technologies. React + Django preferred."
    }')
echo "Job 3 created: $JOB3_RESPONSE"

# Create another company and job
echo "5. Creating second company..."
COMPANY2_RESPONSE=$(curl -s -X POST "$API_BASE/users/register/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "tech_company",
        "email": "hr@techcompany.test",
        "password": "testpass123",
        "is_company": true,
        "company": "Tech Solutions Inc"
    }')
echo "Second company created: $COMPANY2_RESPONSE"

# Login as second company
curl -s -X POST "$API_BASE/users/login/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "tech_company",
        "password": "testpass123"
    }' \
    -c company2_cookies.txt > /dev/null

# Create job for second company
JOB4_RESPONSE=$(curl -s -X POST "$API_BASE/jobs/" \
    -H "Content-Type: application/json" \
    -b company2_cookies.txt \
    -d '{
        "title": "DevOps Engineer",
        "salary": "75000",
        "company": "Tech Solutions Inc",
        "status": "Open",
        "experience": 3,
        "description": "Looking for a DevOps Engineer with experience in AWS, Docker, and Kubernetes. CI/CD pipeline experience required."
    }')
echo "Job 4 created: $JOB4_RESPONSE"

echo ""
echo "✅ Test data setup complete!"
echo ""
echo "📋 Available test accounts:"
echo "👤 Regular User: frontend_test_user / testpass123"
echo "🏢 Company 1: frontend_test_company / testpass123 (Frontend Test Corp)"
echo "🏢 Company 2: tech_company / testpass123 (Tech Solutions Inc)"
echo ""
echo "🔗 Test these pages:"
echo "• http://localhost:8080/signup.html"
echo "• http://localhost:8080/login.html"
echo "• http://localhost:8080/features/user/search_jobs.html"
echo "• http://localhost:8080/features/admin/dashboard.html"
echo ""
echo "🧪 Now test the frontend integration!"

# Clean up cookies
rm -f company_cookies.txt company2_cookies.txt
