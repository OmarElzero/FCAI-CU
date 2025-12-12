# 🧪 Frontend Integration Testing Guide

## Overview
This guide helps you systematically test all frontend features with the Django backend API.

## Testing Checklist

### 📋 **Pre-Testing Setup**
- [x] Django backend running on http://localhost:8000
- [x] Frontend server running on http://localhost:8080
- [x] API endpoints tested and working
- [x] CORS configured properly

### 🎯 **Testing Scenarios**

## 1. 👤 **User Authentication Tests**

### Test 1.1: User Registration
**Regular User:**
1. Go to: http://localhost:8080/signup.html
2. Fill form:
   - Username: `testuser_frontend`
   - Email: `testuser@frontend.com`
   - Password: `password123`
   - Confirm Password: `password123`
   - Leave "Register as Company Admin" unchecked
3. Click "Create Account"
4. **Expected:** Success message, redirect to search jobs page

**Company User:**
1. Go to: http://localhost:8080/signup.html
2. Fill form:
   - Username: `companyuser_frontend`
   - Email: `company@frontend.com`
   - Password: `password123`
   - Confirm Password: `password123`
   - Check "Register as Company Admin"
   - Company Name: `Frontend Test Company`
3. Click "Create Account"
4. **Expected:** Success message, redirect to admin dashboard

### Test 1.2: User Login
**Regular User Login:**
1. Go to: http://localhost:8080/login.html
2. Enter:
   - Username: `testuser_frontend`
   - Password: `password123`
3. Click "Sign In"
4. **Expected:** Redirect to search jobs page

**Company User Login:**
1. Go to: http://localhost:8080/login.html
2. Enter:
   - Username: `companyuser_frontend`
   - Password: `password123`
3. Click "Sign In"
4. **Expected:** Redirect to admin dashboard

### Test 1.3: Authentication State
1. After login, check:
   - Navbar shows user-specific options
   - User name displayed in navbar
   - Logout option available
2. Try accessing protected pages directly
3. **Expected:** Proper authentication state maintained

## 2. 💼 **Job Management Tests (Company Users)**

### Test 2.1: Job Creation
1. Login as company user
2. Go to: Admin Dashboard → Add Job
3. Fill job form:
   - Title: `Frontend Test Job`
   - Salary: `70000`
   - Company: `Frontend Test Company`
   - Experience: `2`
   - Description: `This is a test job created from frontend`
4. Click "Post Job"
5. **Expected:** Job created successfully, redirect to dashboard

### Test 2.2: Job Listing (Admin View)
1. Go to admin dashboard
2. Check if created jobs appear in the list
3. Verify job details are correct
4. **Expected:** All created jobs displayed with correct information

### Test 2.3: Job Editing
1. From admin dashboard, click "Edit" on a job
2. Modify job details
3. Save changes
4. **Expected:** Job updated successfully

### Test 2.4: View Applicants
1. From admin dashboard, click "View Applicants" on a job
2. Check applicant list
3. **Expected:** List of applicants (if any) displayed correctly

## 3. 🔍 **Job Search Tests (Regular Users)**

### Test 3.1: Job Listing
1. Login as regular user
2. Go to: Search Jobs page
3. **Expected:** List of all available jobs displayed

### Test 3.2: Job Search & Filtering
1. On search jobs page:
   - Try searching by keyword
   - Try filtering by experience level
   - Try filtering by company
2. **Expected:** Results filtered correctly

### Test 3.3: Job Details
1. Click on a job from the list
2. **Expected:** Job details page opens with full information

## 4. 📄 **Job Application Tests (Regular Users)**

### Test 4.1: Apply for Job
1. Login as regular user
2. Go to job details page
3. Click "Apply Now"
4. **Expected:** Application submitted successfully

### Test 4.2: View Applied Jobs
1. Go to: Applied Jobs page
2. **Expected:** List of jobs user has applied to

### Test 4.3: Application Status
1. Check application status in applied jobs
2. **Expected:** Status shows correctly (pending, accepted, rejected)

## 5. 🌐 **Navigation & UI Tests**

### Test 5.1: Navbar Functionality
1. Test all navbar links
2. Check user menu dropdown
3. Test logout functionality
4. **Expected:** All navigation works correctly

### Test 5.2: Responsive Design
1. Test on different screen sizes
2. Check mobile navigation
3. **Expected:** Site responsive on all devices

### Test 5.3: Error Handling
1. Try submitting forms with invalid data
2. Try accessing pages without authentication
3. **Expected:** Proper error messages displayed

## 6. 🔧 **API Integration Tests**

### Test 6.1: Real-time Updates
1. Create job as company user
2. Login as regular user in another tab
3. Check if new job appears without refresh
4. **Expected:** Data updates properly

### Test 6.2: Session Management
1. Login and stay idle
2. Try performing actions after some time
3. **Expected:** Session handled correctly

### Test 6.3: Error Handling
1. Stop backend server
2. Try using frontend features
3. **Expected:** Graceful error handling

## 🐛 **Common Issues to Check**

1. **CORS Errors:** Check browser console for CORS issues
2. **Authentication Issues:** Verify cookies are being set
3. **API Endpoint Errors:** Check network tab for failed requests
4. **JavaScript Errors:** Check browser console for JS errors
5. **Form Validation:** Test all form validations work

## 📊 **Testing Tools**

1. **API Test Console:** http://localhost:8080/api-test-console.html
2. **Browser DevTools:** Network and Console tabs
3. **Backend Admin:** http://localhost:8000/admin/ (if superuser created)

## ✅ **Success Criteria**

- [ ] All user registration flows work
- [ ] All login flows work
- [ ] Job creation works for company users
- [ ] Job search and filtering work for regular users
- [ ] Job applications work for regular users
- [ ] Navigation and UI work properly
- [ ] Error handling works correctly
- [ ] API integration is seamless

## 🚨 **If Issues Found**

1. Check browser console for errors
2. Check network tab for failed API calls
3. Verify backend server is running
4. Check API endpoint responses
5. Review authentication state
6. Test with API console first

---

**Next Steps After Testing:**
1. Document any bugs found
2. Fix critical issues
3. Optimize performance
4. Prepare for production deployment
