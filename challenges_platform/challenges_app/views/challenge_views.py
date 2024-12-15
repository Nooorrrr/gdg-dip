from django.http import  JsonResponse
from django.views.decorators.csrf  import csrf_exempt # for cookies 
from django.contrib.auth.decorators import login_required
from challenges_app.models import  Challenge
import json
from django.core.paginator import Paginator

# the first function is listing all challenges to all the users 
# @login_required
# @csrf_exempt
def list_challenges(request):
    if request.method == 'GET':
        #retrieving all the challenges 
        challenges = Challenge.objects.all()

       
         # Pagination
        paginator = Paginator(challenges, 10)  # Show 10 submissions per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #organizing the challenges list in a json dictionary
        challenges_list = []
        for challenge in challenges:
            challenges_list.append({
                'id': challenge.id,
                'title': challenge.title,
                'description': challenge.description,
                'resources': challenge.resources,
                'status': challenge.status
            })

    
        # Return the paginated submissions list in JSON format
        return JsonResponse({
            'challenges': challenges_list,
            'total_pages': paginator.num_pages,  
            'current_page': page_obj.number,    
            'has_next': page_obj.has_next(),    
            'has_previous': page_obj.has_previous(),  
        }, status=200)
        
        
        
    return JsonResponse({'error': 'Invalid request method'},status=405)

# adding a challenge for the admin only 
@login_required
@csrf_exempt
def add_challenge(request):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Invalid request method'},status=403)
        
        # get the  data from the request
        data = json.loads(request)
        title = data.get('title')
        description = data.get('description')
        resources = data.get('resources')
        status = False 
        # the id is autoincremented 
        # we need to remove the id from the model, so django consider the incrementation by default 
        #create the challenge 
        challenge = Challenge.objects.create(
            title=title,
            description=description,
            resources=resources,
            status=status
        )


        return JsonResponse({'message': 'Challenge successfully added!', 'challenge_id': challenge.id}, status=201)


    return JsonResponse({'error': 'Invalid request method'},status=405)

# updating and editing a challenge 
@login_required
@csrf_exempt
def update_challenge(request):
    if request.method == 'PUT' or request.method == 'PATCH':
        if not request.user.is_superuser:
            return JsonResponse({'error': 'You are not authorized to update challenges'}, status=403)

        # Get the challenge ID and the new data
        data = json.loads(request.body)
        challenge_id = data.get('challenge_id')
        title = data.get('title')
        description = data.get('description')
        resources = data.get('resources')

        # check if the challenge exists in the database 
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            return JsonResponse({'error': 'Challenge does not exist'}, status=404)

        if title:
            challenge.title = title
        if description:
            challenge.description = description
        if resources:
            challenge.resources = resources
        
        #saving the challenge
        challenge.save()

        return JsonResponse({'message': 'Challenge successfully updated!'}, status=200)
    return JsonResponse({'error': 'Invalid request method'},status=405)

# deleting a challenge by the admins
@login_required
@csrf_exempt
def delete_challenge(request):
    if request.method == 'DELETE':
        if not request.user.is_superuser:
            return JsonResponse({'error': 'you are not autherized for this action'}, status=403)
        
        # else get the challenge id 
        data = json.loads(request)
        challenge_id = data.get('challenge_id')

        # check if the challenge exists
        try:
            challenge_id = int(challenge_id)
            challenge = Challenge.objects.get(id = challenge_id)
        except Challenge.DoesNotExist:
            return JsonResponse({'error': 'challenge was not found'}, status=404)

        # removing the challenge 
        challenge.delete()
    
        return JsonResponse({'messgae': 'the challenge was deleted successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# assignment of a challenge to a team 
