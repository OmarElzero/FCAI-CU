# Configuration file for Student Data Fetcher
# Update the token here when it expires

API_CONFIG = {
    "base_url": "http://193.227.14.58/api/student-courses",
    "token": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIyMDIzMDI2MyIsImF1dGgiOiJST0xFX1NUVURFTlQiLCJleHAiOjE3NTQ2OTMwOTh9.BzjnOzZ4LlMAxJIcbD7GRt-3EK1giwrGmpmmM_xPBq0RoSJ1FL6QbNJeivw45a3aqH2NTijNF6-FhWOsgY8mUg",
    "page_size": 2000,
    "timeout": 60,
    "max_retries": 3,
    "delay_between_requests": 0.3
}

# Update instructions:
# 1. When the token expires, replace the "token" value above
# 2. Make sure to include "Bearer " at the beginning
# 3. The token is the JWT token from your browser's developer tools
# 4. You can also adjust other settings like page_size if needed
