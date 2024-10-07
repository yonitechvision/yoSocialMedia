### Social Media API Project

# Overview

This project is a Social Media API built using Django and Django REST Framework. It provides key features commonly found in social media platforms, such as:

User Authentication (Signup, Login, JWT-based Authentication)
Post Management (Create, Edit, Delete, Like, Repost)
Followers (Follow/Unfollow users)
Notifications (Real-time notifications for actions like follows, likes, and comments)
Direct Messaging (User-to-user messaging)
Video Calls (WebRTC-based peer-to-peer video calling)
Hashtags (Use of hashtags to categorize posts)
Trending Posts (Popular posts based on likes and reposts)
The back-end is built using Django Channels for real-time WebSocket connections, Django REST Framework for API functionality, and JWT (JSON Web Tokens) for authentication. The API serves as the foundation for a front-end to consume via RESTful endpoints.

## Key Features

JWT Authentication: Secure token-based authentication using Django REST Framework SimpleJWT.
Real-time WebSocket Support: Handle real-time events like messaging and video calls.
Profile Customization: Users can customize their profiles, including profile pictures, bio, and cover photos.
Post and Hashtag Support: Users can create posts, like, share, and tag posts using hashtags.
Video Calling: Users can initiate peer-to-peer video calls using WebRTC.
Notification System: Get notifications when someone interacts with your posts or follows you.

## Technologies Used

Django: The web framework used for the project.
Django REST Framework: For creating RESTful APIs.
Django Channels: For WebSocket connections and real-time communication.
SimpleJWT: For token-based authentication using JSON Web Tokens (JWT).
SQLite: Database used for development purposes (can be switched to PostgreSQL or MySQL for production).
WebRTC: For handling peer-to-peer video calls.
Redis (optional for production): Used with Django Channels to handle real-time WebSocket communication at scale.

## Project Setup and Project Structure


SocialMediaRobust/
│
├── api/                            # Your app (contains models, views, serializers, etc.)
│   ├── migrations/                 # Migrations for your models
│   ├── __init__.py                 # App initialization file
│   ├── admin.py                    # Admin configurations (optional)
│   ├── apps.py                     # App configurations
│   ├── models.py                   # All your database models (Profile, Post, Like, etc.)
│   ├── serializers.py              # Serializers to convert models to JSON
│   ├── views.py                    # View logic (User, Post, Like, Follow, etc.)
│   ├── urls.py                     # URLs specific to this app
│   ├── tests.py                    # Unit tests (if any)
│   ├── consumers.py                # WebSocket consumers for handling video calls
│
├── media/                          # Local media storage (created when you upload files)
│   ├── profiles/                   # Profile pictures will be saved here
│   ├── cover_photos/               # Cover photos will be saved here
│   └── uploads/                    # Media files related to posts (images/videos) saved here
│
├── socialMediaAPI/                 # Project settings folder (project-wide configs)
│   ├── __init__.py                 # Project initialization
│   ├── asgi.py                     # ASGI configuration (optional)
│   ├── settings.py                 # Project-wide settings (database, REST framework, media)
│   ├── urls.py                     # Root URL configuration (includes API URLs)
│   ├── wsgi.py                     # WSGI configuration for deployment
│   ├── routing.py                  # WebSocket routing configuration for Channels
│
├── manage.py                       # Django's CLI utility for running commands
├── db.sqlite3                      # Your local SQLite database file (auto-generated)
├── requirements.txt                # Your project’s dependencies (e.g., djangorestframework, etc.)
└── README.md                       # Project description and setup instructions


## 1. Clone the Repository
First, clone the project repository to your local machine:

bash
Copy code
# git clone https://github.com/your-username/SocialMediaAPI.git
cd SocialMediaAPI

## 2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment as follows:

bash
Copy code
# Create virtual environment
python -m venv venco

# Activate virtual environment (Windows)
venco\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venco/bin/activate


## 3. Install Dependencies

bash
Copy code
pip install django djangorestframework channels djangorestframe-simplejwt
# Install the required Python packages using pip:
pip install -r requirements.txt
This will install all dependencies, including Django, Django REST Framework, Django Channels, and SimpleJWT.

## 4. Set Up Environment Variables
Create a .env file in the project’s root directory to manage sensitive information, such as your secret key and database credentials. Add the following:

env
Copy code
SECRET_KEY=your-django-secret-key
DEBUG=True
For production, remember to set # DEBUG=False and configure the allowed hosts.

## 5. Database Setup
By default, the project uses SQLite for development. You can initialize the database using the following commands:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
If you plan to switch to PostgreSQL or another database for production, update the DATABASES setting in settings.py accordingly.



## 6. Create a Superuser
To access the admin panel and manage the application, you need to create a superuser:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to set up your admin credentials.

## 7. Running the Application
To run the development server, execute the following command:

bash
Copy code
python manage.py runserver
The server will be running at http://127.0.0.1:8000/.

## JWT Authentication
Getting Access and Refresh Tokens
Login Endpoint: POST /api/token/
Send a POST request with your username and password in the body to get access and refresh tokens.

Refresh Token Endpoint: POST /api/token/refresh/
Send the refresh token to this endpoint to receive a new access token.

Example request body:

json
Copy code
{
  "username": "your-username",
  "password": "your-password"
}
# Key Endpoints
Below are some key endpoints provided by the API:

User Signup: POST /api/signup/
User Login: POST /api/token/
Create Post: POST /api/posts/
List Posts: GET /api/posts/
Follow User: POST /api/followers/follow/
Unfollow User: POST /api/followers/unfollow/
Video Call Initiation (WebSocket): ws://127.0.0.1:8000/ws/call/<ChatVideo>/
Send Direct Message: POST /api/messages/
Refer to the full API documentation for more details.

### Here's a detailed list of all key endpoints available in my social media API, covering user management, posts, likes, comments, followers, direct messages, notifications, reposts, hashtags, video calls, and more.

## Key Endpoints and How to Test Them

# 1. User Authentication & Management

# a. User Signup
Endpoint: POST /api/signup/
Description: Allows users to sign up.
Request Body:
json
# Copy code
{
    "username": "exampleUser",
    "password": "password123!",
    "email": "user@example.com"
}
# Expected Response:
json
# Copy code
{
    "message": "User created successfully"
}

# b. User Login (JWT Token Generation)

Endpoint: POST /api/token/
Description: Allows users to log in and receive JWT tokens.
# Request Body:
json
# Copy code
{
    "username": "exampleUser",
    "password": "password123!"
}
#Expected Response:
json
Copy code
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}

# 2. Profile Management

# a. Create Profile
Endpoint: POST /api/profiles/
Description: Creates a profile for the logged-in user.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "bio": "Hello! I'm a new user.",
    "location": "New York",
    "website": "http://example.com"
}

# b. View All Profiles
Endpoint: GET /api/profiles/
Description: Lists all profiles.
Headers: Authorization: Bearer <access_token>
c. Retrieve or Update a Specific Profile
Endpoint: GET /api/profiles/<profile_id>/
Description: Retrieve or update a user profile.
Headers: Authorization: Bearer <access_token>

# 3. Posts

# a. Create a Post
Endpoint: POST /api/posts/
Description: Allows authenticated users to create posts.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "content": "My first post!",
    "media": "<media_file>" // Optional (multipart/form-data)
}

# b. List All Posts
Endpoint: GET /api/posts/
Description: Retrieves all posts from all users.
# c. View or Update a Specific Post
Endpoint: GET /api/posts/<post_id>/
Description: View or update a specific post.
# d. User Feed
Endpoint: GET /api/posts/feed/
Description: Retrieves posts from users the authenticated user follows.
Headers: Authorization: Bearer <access_token>

# 4. Likes

# a. Like a Post
Endpoint: POST /api/likes/
Description: Allows a user to like a post.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "post": 1 // ID of the post to like
}

# 5. Comments

# a. Comment on a Post
Endpoint: POST /api/comments/
Description: Allows a user to comment on a post.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "post": 1,
    "content": "Great post!"
}

# 6. Followers

# a. Follow a User
Endpoint: POST /api/followers/follow/
Description: Allows a user to follow another user.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "user_to": 2 // ID of the user to follow
}
# b. Unfollow a User
Endpoint: POST /api/followers/unfollow/
Description: Allows a user to unfollow another user.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "user_to": 2 // ID of the user to unfollow
}

# 7. Direct Messaging

# a. Send a Direct Message
Endpoint: POST /api/messages/
Description: Send a message to another user.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "recipient": 2,  // ID of the recipient user
    "content": "Hey there!"
}
# b. View Sent and Received Messages
Endpoint: GET /api/messages/
Description: Retrieve messages sent or received by the authenticated user.

# 8. Notifications

# a. View Notifications
Endpoint: GET /api/notifications/
Description: View all notifications for the authenticated user.
Headers: Authorization: Bearer <access_token>
# b. Mark Notification as Read
Endpoint: POST /api/notifications/<notification_id>/read/
Description: Mark a specific notification as read.

# 9. Reposts

# a. Repost a Post
Endpoint: POST /api/reposts/
Description: Allows a user to repost a post.
Headers: Authorization: Bearer <access_token>
Request Body:
json
Copy code
{
    "post": 1 // ID of the post to repost
}

# 10. Hashtags

# a. List Hashtags
Endpoint: GET /api/hashtags/
Description: Retrieve all available hashtags.
# b. View Posts for a Specific Hashtag
Endpoint: GET /api/hashtags/<hashtag_id>/
Description: Retrieve posts tagged with a specific hashtag.
# 11. Trending Posts

# a. View Trending Posts
Endpoint: GET /api/posts/trending/
Description: Retrieve trending posts based on likes or reposts.

# 12. Video Calls

# a. Initiate Video Call
Endpoint: ws://127.0.0.1:8000/ws/call/<ChatVideo>/
Description: WebSocket endpoint for authenticated users to join or initiate a video call.
Note: Ensure you pass a valid access_token as a query parameter or header when connecting to the WebSocket.
How to Test
Use Postman or a similar tool to test the endpoints.
Make sure to set Authorization headers properly for authenticated endpoints.
For WebSocket testing, tools like WebSocket King or similar can help simulate WebSocket connections.
By covering these endpoints, you should have a comprehensive guide to interacting with all aspects of the social media API, including managing users, creating posts, engaging with content, following other users, messaging, and using video calls.

## Deployment

# 1. Set Up Production Environment

For production, switch your database to PostgreSQL, and update the settings.py file with production settings:

python
Copy code
DEBUG = False
ALLOWED_HOSTS = ['your-production-domain.com']

# 2. Configure Static and Media Files
Collect static files for production:

bash
Copy code
python manage.py collectstatic
Make sure to set up a cloud storage service (like AWS S3) or configure static file handling on your server.

# 3. Configure WebSockets with Django Channels
For production, it’s recommended to use Redis as the channel layer for handling WebSockets.

# Install Redis:

bash
Copy code
pip install channels_redis
Update settings.py:

python
Copy code
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
Run Redis on your server to handle WebSocket communications.

# 4. Deploy with Gunicorn and Daphne
Use Gunicorn for handling HTTP requests and Daphne for WebSocket connections.

bash
Copy code
# Install daphne and gunicorn
pip install gunicorn daphne

# Run daphne to serve the app
daphne -u /tmp/daphne.sock SocialMediaAPI.asgi:application

# Run gunicorn to handle HTTP requests
gunicorn --workers 3 SocialMediaAPI.wsgi
# 5. Domain and SSL Setup
Use NGINX or Apache to serve your app in production. Don't forget to secure your application with SSL using Let's Encrypt or another certificate authority.

### Conclusion
This Social Media API offers a robust back-end infrastructure for a social media platform. The real-time functionality provided by Django Channels and WebSockets, coupled with token-based authentication using JWT, makes it an ideal project for building scalable social media applications.