from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from challenges_app.models import Team, Challenge, Submission
import json

@login_required
@csrf_exempt
def create_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        team_name = data.get('name')
        members_emails = data.get('members', '')  # Comma-separated list of user emails
        # there will be no challenge assigned to the team by defult 

        # Check if the necessary data is provided
        if not team_name or not members_emails :
            return JsonResponse({'error': 'Missing required fields, the team name and the members'}, status=400)

        # Check if the user is the team leader of any team (if they already lead one)
        if Team.objects.filter(team_leader=request.user).exists():
            return JsonResponse({'error': 'You are already leading a team'}, status=400)

        
        # Parse the comma-separated list of user emails
        members_emails_list = [email.strip() for email in members_emails.split(',') if email.strip()]

        # Check if all users with the provided emails exist
        members = []
        for email in members_emails_list:
            try:
                user = User.objects.get(email=email)
                members.append(user)
            except User.DoesNotExist:
                return JsonResponse({'error': f'User with email {email} does not exist'}, status=400)

        # Create the team
        team = Team.objects.create(
            team_leader = request.user,
            name=team_name,
        )

        # Assign members to the team and set their team_id
        for member in members:
            member.team_id = team.id  # Assigning the team ID to each member
            member.save()

        # Respond with success and the team details
        return JsonResponse({
            'message': 'Team successfully created!',
            'team_id': team.id,
            'team_name': team.name,
            'team_leader': team.team_leader.username,
            'challenge_id': team.challenge.id,
            'members': [member.username for member in team.members.all()]
        }, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# getting the infos of a team (the team space)
@login_required
def team_space_info(request,team_id):
# Check if the request method is GET
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        # Retrieve the team using the provided team_id
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    # Check if the user is the team leader, a member of the team, or an admin
    if request.user.team_id != team.id :
        return JsonResponse({'error': 'You are not authorized to view this team'}, status=403)

    members = User.objects.filter(team_id=team.id)

    # Get the team leader information
    team_leader = team.team_leader.name if team.team_leader else None  # Username of the team leader

    # Get the challenge and submission objects using their respective ids
    challenge = None
    submission = None
    if team.challenge_id:
        try:
            challenge = Challenge.objects.get(id=team.challenge_id)
        except Challenge.DoesNotExist:
            return JsonResponse({'error': 'Challenge not found'}, status=404)

    if team.submission_id:
        try:
            submission = Submission.objects.get(id=team.submission_id)
        except Submission.DoesNotExist:
            return JsonResponse({'error': 'Submission not found'}, status=404)

    # Prepare the response data
    team_info = {
        'team_id': team.id,
        'team_name': team.name,
        'team_leader': team_leader,  # Team leader username
        'members': [member.name for member in members],  # List all member usernames
    }

    # If a challenge is assigned, return its full details
    if challenge:
        team_info['challenge'] = {
            'id': challenge.id,
            'title': challenge.title,
            'category': challenge.category,
            'description': challenge.description,
            'resources': challenge.resources,
            'status': challenge.status
        }

    # If a submission exists, return its full details
    if submission:
        team_info['submission'] = {
            'id': submission.id,
            'team_id': submission.team_id,
            'challenge_id': submission.challenge_id,
            'video_url': submission.video_url,
            'resources_links': submission.resources_links,
        }

    # Return the team information as a JSON response
    return JsonResponse({'team_info': team_info}, status=200)


# and thats it for the team space