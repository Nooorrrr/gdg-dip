# API Endpoints Documentation

## **Challenges**

1. **`GET /challenges/`** – Lists all available challenges.
   - **Functionality**: Displays a list of challenges available in the system.
   - **View**: `list_challenges`

2. **`POST /challenges/add/`** – Adds a new challenge (accessible only by superusers).
   - **Functionality**: Allows superusers to create and add a new challenge to the system.
   - **View**: `add_challenge`

3. **`PUT/PATCH /challenges/update/`** – Updates an existing challenge (accessible only by superusers).
   - **Functionality**: Allows superusers to modify an existing challenge.
   - **View**: `update_challenge`

4. **`DELETE /challenges/delete/`** – Deletes a challenge (accessible only by superusers).
   - **Functionality**: Allows superusers to remove an existing challenge from the system.
   - **View**: `delete_challenge`

5. **`POST /challenges/assign/`** – Assigns a challenge (accessible only by superusers).
   - **Functionality**: Allows superusers to assign a challenge to a specific user or group.
   - **View**: `assign_challenge`

---

## **Submissions**

1. **`POST /submissions/add/`** – Adds a new submission (accessible by team leaders).
   - **Functionality**: Allows team leaders to submit their solutions or answers to a challenge.
   - **View**: `add_submission`

2. **`DELETE /submissions/remove/`** – Removes an existing submission.
   - **Functionality**: Allows removal of a previously submitted solution or answer.
   - **View**: `delete_submission`

3. **`PUT/PATCH /submissions/update/`** – Updates an existing submission.
   - **Functionality**: Allows the modification of an existing submission.
   - **View**: `update_submission`

4. **`GET /submissions/`** – Retrieves all submissions (accessible by admin users).
   - **Functionality**: Admin users can view all submitted solutions or answers for challenges.
   - **View**: `get_submissions`

---

## **Teams**

1. **`POST /teams/create/`** – Creates a new team.
   - **Functionality**: Allows users to create a new team for participating in challenges.
   - **View**: `create_team`

2. **`GET /teams/<int:team_id>/info/`** – Retrieves the information of a specific team.
   - **Functionality**: Allows users to view detailed information about a specific team.
   - **View**: `team_space_info`

3. **`POST /teams/leave/`** – Allows a user to leave a team.
   - **Functionality**: Allows users to exit a team they are currently a part of.
   - **View**: `leave_team`

4. **`POST /teams/<int:team_id>/join/`** – Allows a user to join a team.
   - **Functionality**: Allows users to join a specific team using the team's ID.
   - **View**: `join_team`

---

## **Authentication**

1. **`POST /login/`** – Logs in a user.
   - **Functionality**: Allows users to log in to their account.
   - **View**: `login`

2. **`POST /login_admin/`** – Logs in an admin user.
   - **Functionality**: Allows admins to log in to the admin interface.
   - **View**: `admin_login`

3. **`POST /signup/`** – Registers a new user.
   - **Functionality**: Allows a new user to sign up for an account.
   - **View**: `signup`

4. **`GET /test_token/`** – Tests a token.
   - **Functionality**: Allows users to test the validity of their authentication token.
   - **View**: `test_token`
message.txt