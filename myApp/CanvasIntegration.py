import requests

def canvas_api_request(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return None

# Replace these variables with your Canvas API and OAuth2 access token details
canvas_api_url = "https://your-canvas-instance/api/v1"
access_token = "your-access-token"

# Replace with the course ID and user ID you retrieved from the LTI launch
course_id = "your-course-id"
user_id = "your-user-id"

# Get the list of users in your course
users_url = f"{canvas_api_url}/courses/{course_id}/users?access_token={access_token}"
users = canvas_api_request(users_url)

if users:
    for user in users:
        user_id = user.get("id")
        print(f"User ID: {user_id}, Name: {user.get('name')}")

        # Get assignments for each user
        assignments_url = f"{canvas_api_url}/courses/{course_id}/users/{user_id}/assignments?access_token={access_token}"
        assignments = canvas_api_request(assignments_url)

        if assignments:
            for assignment in assignments:
                submission_status = "Not Submitted"
                if "has_submitted_submissions" in assignment:
                    submission_status = "Submitted"
                print(f"Assignment: {assignment.get('name')}, Submission Status: {submission_status}")
        else:
            print("No assignments found for this user.")
else:
    print("No users found in the course.")
