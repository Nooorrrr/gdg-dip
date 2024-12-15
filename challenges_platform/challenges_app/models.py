from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# the challenge class
class Challenge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    resources = models.URLField(blank=True)
    status = models.BooleanField(default=False)

# the team class 
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    submission_id = models.ForeignKey('Submission', related_name='teams', on_delete=models.SET_NULL, null=True, blank=True)
    challenge_id = models.ForeignKey('Challenge', 
        on_delete=models.SET_NULL, 
        null=True
    )

# the users class
   
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    team_id = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL) 
    def __str__(self):
        return self.user.username
    
   

# the submissions class
class Submission(models.Model):
    challenge_id = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team,on_delete=models.CASCADE)
    video_url = models.URLField()
    resources_links = models.TextField()
