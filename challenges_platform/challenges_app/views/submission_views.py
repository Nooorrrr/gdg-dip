from django.shortcuts import render
from django.http import  JsonResponse
from django.views.decorators.csrf  import csrf_exempt # for cookies 
from django.contrib.auth.decorators import login_required
from challenges_app.models import Submission, Team, Challenge
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator


#  ensuring that the user is logged in

# submitting a soluton for  team
@login_required
@csrf_exempt 
def add_submission(request):
    if request.method == 'POST':
        
        # get the data from the request 
        data = json.loads(request.body)
        team_id = data.get('team_id')
        challenge_id = data.get('challenge_id')
        video_url = data.get('video_url')
        resources_links = data.get('resources_links')
       

         # Check if all required fields are provided (we can do a check in the fronetned to)
        if not all([team_id, challenge_id, video_url, resources_links]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        

        try:
            # Validate challenge_id exists
            challenge = Challenge.objects.get(id=challenge_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Challenge does not exist'}, status=400)

        # Validate team_id exists
        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Team does not exist'}, status=400)


        # if the user is not the team lead then return an error 
        if team.team_leader != request.user:
            return JsonResponse({
                'message': 'You are not the team lead, cannot add submission.',
            },status=403
            )

       # else build the submission object and insert it into the database
        submission = Submission.objects.create(
            challenge_id=challenge.id,  # Pass the challenge ID to the foreign key
            team_id=team.id,            # Pass the team ID to the foreign key
            video_url=video_url,
            resources_links=resources_links
        )

        # Respond with success message
        return JsonResponse(
            {'message': 'Submission successfully added!' ,'submission_id': submission.id}, status=201
        )

        
    # if the method is not a post request 
    return JsonResponse({'messgae' : 'invalid request method'},status=405)

# removing a submission
@login_required
@csrf_exempt
def remove_submission(request):
    if request.method == 'DELETE':

        #get the submission ID
        data = json.loads(request.body)
        submission_id = data.get('submission_id')


        if not submission_id:
            return JsonResponse({'error' : 'invalid submission'},status=405)
        
        # fetch the submission object from the database 
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return JsonResponse({'error' : 'Submission does not exist'},status=405)

        # check if the current user is the team leader
        team = submission.team_id
        if team.team_leader != request.user and not request.user.is_admin:
            return JsonResponse({'error' : 'you are not authorized to delete this submission'},status=403)
        
        #deleting the submission
        submission.delete()

        #success
        return JsonResponse({'message': 'Submission successfully deleted!'}, status=200)
    
     # If the method is not a DELETE request
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# updating a submission
@login_required
@csrf_exempt
def update_submission(request):
    if request.method == 'PUT' or request.method == 'PATCH':

        #get the submission ID
        data = json.loads(request.body)
        submission_id = data.get('submission_id')
        video_url = data.get('video_url')
        resources_links = data.get('resources_links')
        # getting all the possible fields to be updated from the request
        # if the fields is not desired to be updated then it will have the value NULL


        if not submission_id:
            return JsonResponse({'error' : 'invalid submission'},status=405)
        
        # fetch the submission object from the database 
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return JsonResponse({'error' : 'Submission does not exist'},status=405)

        # check if the current user is the team leader
        team = submission.team_id
        if team.team_leader != request.user and not request.user.is_admin:
            return JsonResponse({'error' : 'you are not authorized to update this submission'},status=403)
        
        # Update fields if provided in the request body
        if video_url:
            submission.video_url = video_url
        if resources_links:
            submission.resources_links = resources_links

        # Save the updated submission
        submission.save()

        #success
        return JsonResponse({'message': 'Submission successfully updated!'}, status=200)
    
     # If the method is not a DELETE request
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# getting the lists of submissions for the admin user 
@login_required
@csrf_exempt
def get_submissions(request):
    # make sure that the user is authenticated and it is an admin 
    if not request.user.is_admin:
        return JsonResponse({'error': 'you are not authorized to view all the submissions'}, status=403)
    
    if request.method == 'GET':
        #retrieve the list of submissions
        submissions = Submission.objects.all()

        # Pagination
        paginator = Paginator(submissions, 10)  # Show 10 submissions per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #structuring the submissions in a json dictionary
        submissions_list = []
        for submission in submissions:
            submissions_list.append({
                'submission': submission.id,
                'team_id': submission.team_id,
                'challenge_id': submission.challenge_id,
                'video_url': submission.video_url,
                'resources_links': submission.resources_links,
            })

    
        # Return the paginated submissions list in JSON format
        return JsonResponse({
            'submissions': submissions_list,
            'total_pages': paginator.num_pages,  # Include the total number of pages
            'current_page': page_obj.number,     # Include the current page number
            'has_next': page_obj.has_next(),     # Whether there is a next page
            'has_previous': page_obj.has_previous(),  # Whether there is a previous page
        }, status=200)
        
    # If the method is not GET
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# and thats it for the submissions list