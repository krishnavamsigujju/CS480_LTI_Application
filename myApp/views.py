# from django.shortcuts import render
# from django.http import HttpResponse


# Create your views here.
# def index(request):
#     return HttpResponse("Welcome to CSEducation")

# def index(request):
# #retrieved course id and user name to display
#     return HttpResponse("Welcome user: "+request.POST["custom_course_id"]+" to the course with id: "+ request.POST["custom_user_id"])


from django.http import HttpResponse
from django.shortcuts import render
# Import necessary Canvas API classes
from canvasapi import Canvas

def index(request):
    # Canvas API URL
    API_URL = "https://canvas.instructure.com/"

    # Canvas API key
    API_KEY = "7~veaPySTkEmDFUDiNlij52F02lwcczr2sT8vyTO9OZzzkzZoRVPKPM4Av1KfbxGRZ"  # Replace with your Canvas API key

    try:
        # Initialize a new Canvas object
        canvas = Canvas(API_URL, API_KEY)

        # Get the course by course ID
        course = canvas.get_course(7887397)

        # Get a list of users in the course 
        users = course.get_users(enrollment_type=['student'], per_page=100)  # Adjust per_page as needed

        response_message = f"Welcome user: {request.POST['custom_course_id']} to the course with id: {request.POST['custom_user_id']}<br>"

        for user in users:
            response_message += f"User: {user.name}<br>"

            # Get the list of assignments for the user in the course
            user_assignments = user.get_assignments(course.id, per_page=100)  # Adjust per_page as needed

            if user_assignments:
                response_message += "Assignments:<br>"
                for assignment in user_assignments:
                    response_message += f"- Assignment: {assignment.name}<br>"
                    submission = assignment.get_submission(user)
                    if submission and submission.workflow_state == 'submitted':
                        response_message += "  - Submission: Submitted<br>"
                    else:
                        response_message += "  - Submission: Not Submitted<br>"
            else:
                response_message += "No assignments found for this user in the course.<br>"

    except Exception as e:
        response_message = f"An error occurred: {str(e)}<br>"

    # Always return an HttpResponse
    return HttpResponse(response_message)


