#!/bin/bash

# API Endpoint Testing Script for JobSearch Application
echo "🚀 Testing JobSearch API Endpoints"
echo "=================================="

BASE_URL="http://localhost:8000/api"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    local description=$5
    local cookies=$6
    
    echo -e "\n${YELLOW}Testing: $description${NC}"
    echo "Method: $method | Endpoint: $endpoint"
    
    if [ -n "$cookies" ]; then
        response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X $method "$BASE_URL$endpoint" -H "Content-Type: application/json" -b "$cookies" -d "$data")
    else
        response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X $method "$BASE_URL$endpoint" -H "Content-Type: application/json" -d "$data")
    fi
    
    body=$(echo $response | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
    status=$(echo $response | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')
    
    if [ "$status" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ SUCCESS${NC} (Status: $status)"
        echo "Response: $body"
    else
        echo -e "${RED}✗ FAILED${NC} (Expected: $expected_status, Got: $status)"
        echo "Response: $body"
    fi
}

# Clean up old cookies
rm -f cookies.txt company_cookies.txt

echo -e "\n📝 1. TESTING USER REGISTRATION"
test_endpoint "POST" "/users/register/" '{"username": "testuser1", "email": "test1@example.com", "password": "testpass123", "is_company": false}' 201 "Register regular user"

test_endpoint "POST" "/users/register/" '{"username": "companyuser1", "email": "company1@example.com", "password": "companypass123", "is_company": true, "company": "Test Company Ltd"}' 201 "Register company user"

echo -e "\n🔐 2. TESTING USER LOGIN"
# Login regular user and save cookies
curl -s -X POST "$BASE_URL/users/login/" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser1", "password": "testpass123"}' \
    -c cookies.txt > /dev/null

test_endpoint "POST" "/users/login/" '{"username": "testuser1", "password": "testpass123"}' 200 "Login regular user"

# Login company user and save cookies
curl -s -X POST "$BASE_URL/users/login/" \
    -H "Content-Type: application/json" \
    -d '{"username": "companyuser1", "password": "companypass123"}' \
    -c company_cookies.txt > /dev/null

test_endpoint "POST" "/users/login/" '{"username": "companyuser1", "password": "companypass123"}' 200 "Login company user"

echo -e "\n👥 3. TESTING USER MANAGEMENT"
test_endpoint "GET" "/users/" "" 200 "List all users (authenticated)" "cookies.txt"

echo -e "\n💼 4. TESTING JOB MANAGEMENT"
test_endpoint "GET" "/jobs/" "" 200 "List all jobs (unauthenticated)"

# Test job creation with company user
test_endpoint "POST" "/jobs/" '{"title": "Software Developer", "salary": "60000", "company": "Test Company Ltd", "status": "Open", "experience": 2, "description": "Looking for a skilled developer"}' 201 "Create job (company user)" "company_cookies.txt"

test_endpoint "GET" "/jobs/" "" 200 "List jobs after creation"

echo -e "\n📄 5. TESTING APPLICATIONS"
# First, get a job ID from the jobs list
job_response=$(curl -s -X GET "$BASE_URL/jobs/" -H "Content-Type: application/json")
job_id=$(echo $job_response | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$job_id" ]; then
    echo "Found job ID: $job_id"
    test_endpoint "POST" "/applications/" "{\"job\": $job_id, \"status\": \"pending\"}" 201 "Apply for job (regular user)" "cookies.txt"
    
    test_endpoint "GET" "/applications/" "" 200 "List applications (user view)" "cookies.txt"
    
    test_endpoint "GET" "/applications/" "" 200 "List applications (company view)" "company_cookies.txt"
else
    echo -e "${RED}No jobs found to test applications${NC}"
fi

echo -e "\n🚪 6. TESTING LOGOUT"
test_endpoint "POST" "/users/logout/" "" 200 "Logout user" "cookies.txt"

echo -e "\n🔒 7. TESTING AUTHENTICATION RESTRICTIONS"
test_endpoint "GET" "/users/" "" 401 "List users (unauthenticated - should fail)"

test_endpoint "POST" "/jobs/" '{"title": "Unauthorized Job", "salary": "50000", "company": "Test", "status": "Open", "experience": 1, "description": "Should fail"}' 401 "Create job (unauthenticated - should fail)"

echo -e "\n🎉 API TESTING COMPLETE!"
echo "=================================="
