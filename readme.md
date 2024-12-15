# Project Name

This project consists of both the **backend** and **frontend** components. The backend is built using **Django** as the web framework, with **PostgreSQL** as the database. REST APIs are implemented to handle various functionalities such as user authentication, challenge management, team creation, and submissions.

## Technologies Used

### Backend:
- **Django** (version 5.1.4)
- **PostgreSQL** (for database management)
- **Django REST Framework** (for creating APIs)
  
### Dependencies:
To ensure the proper environment setup, make sure to install the following dependencies in the `requirements.txt` file:
- asgiref==3.8.1
- Django==5.1.4
- psycopg2-binary==2.9.10
- python-decouple==3.8
- python-dotenv==1.0.1
- sqlparse==0.5.2
- tzdata==2024.2

## Backend Setup

To run the backend server, follow these steps:

### Step 1: Install dependencies
Make sure to install the required dependencies by running:
```bash
pip install -r requirements.txt
```

### Step 2: Set up Database
Ensure you have **PostgreSQL** installed and running. Set up the database connection in your `settings.py` file.

### Step 3: Apply Migrations
Once the dependencies are installed, run the following commands to apply the migrations and set up your database:

```bash
python manage.py makemigrations 
```
```bash
python manage.py migrate
```

### Step 4: Run the Server
To start the development server, use the following command:

```bash
python manage.py runserver
```


The server will be running at `http://127.0.0.1:8000/`.

---

## Database Models

Here are the models created for the application:

### **Challenge Model**
This model represents a challenge in the system.

```python
class Challenge(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    resources = models.URLField(blank=True)
    status = models.BooleanField(default=False)
    inserted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

```
Team Model
This model represents a team participating in challenges.

```python
    class Team(models.Model):
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    submission_id = models.ForeignKey('Submission', related_name='teams', on_delete=models.SET_NULL, null=True, blank=True)
    team_password = models.CharField(max_length=255)
    challenge_id = models.ForeignKey('Challenge', on_delete=models.SET_NULL, null=True)
```
UserProfile Model
This model extends the default User model to store additional information for each user.
```python

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    team_id = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
```

Submission Model
This model represents a submission for a challenge by a team.
```python
    class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    video_url = models.URLField()
    resources_links = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
```


    The auth_user model (built-in Django model) is used to handle user authentication and superuser management for added security.

This `README.md` file includes all the necessary information to run and understand the project, including the backend setup, database models, views, authentication, and frontend interaction. Feel free to modify or add details as needed.
