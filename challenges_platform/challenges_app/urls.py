from django.urls import path
from . import views

urlpatterns = [
    # URL for listing challenges
    path('challenges/', views.list_challenges, name='list_challenges'),

    # URL for adding a new challenge (only for superusers)
    path('challenges/add/', views.add_challenge, name='add_challenge'),

    # URL for updating a challenge (only for superusers)
    path('challenges/update/', views.update_challenge, name='update_challenge'),

    # URL for deleting a challenge (only for superusers)
    path('challenges/delete/', views.delete_challenge, name='delete_challenge'),



    # Add a new submission (POST request)
    path('submissions/add/', views.add_submission, name='add_submission'),
    
    # Remove an existing submission (DELETE request)
    path('submissions/remove/', views.remove_submission, name='remove_submission'),
    
    # Update an existing submission (PUT or PATCH request)
    path('submissions/update/', views.update_submission, name='update_submission'),

    # Get all submissions (GET request for admin users)
    path('submissions/', views.get_submissions, name='get_submissions'),



    # Create a new team (POST request)
    path('teams/create/', views.create_team, name='create_team'),
    
    # Get the information of a specific team (GET request)
    path('teams/<int:team_id>/', views.team_space_info, name='team_space_info'),

]
