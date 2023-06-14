# Helmet Web Application Documentation
## Table of Contents
    ### Introduction
        - Features
        - Installation
        - Prerequisites
        - Cloning the Repository
        - Setting up the Environment
        - Usage
        - Signin and Sign up
        - Add Post
        - Add Event
        - Register for Event
        - View All Posts
        - View All Events
        - Search for Events
        - Search for Posts
        - Conclusion

## 1. Introduction
    Helmet is a Flask web application hosted on Render that allows users to report problems in their communities, schedule events, and register for those events. It serves as a platform for users to voice their concerns and connect with others in their communities.

## 2. Features
    The Helmet web application provides the following features:
    - Signin and Sign up: Users can create an account and sign in to the application.
    - Add Post: Users can create and publish posts to report problems or share information.
    - Add Event: Users can create and schedule events in their communities.
    - Register for Event: Users can register and sign up for events created by others.
    - View All Posts: Users can view all published posts on the application.
    - View All Events: Users can browse and view all scheduled events.
    - Search for Events: Users can search for specific events based on keywords or filters.
    - Search for Posts: Users can search for specific posts based on keywords or filters.

## 3. Installation
    Follow the step-by-step instructions below to install the Helmet web application from the public GitHub repository.

    ### 3.1 Prerequisites
        Before starting the installation, ensure that you have the following prerequisites:
        Python 3.x installed on your system
        Git installed on your system
        Virtual environment tool (e.g., venv, virtualenv) installed
        Integrated Development Environment (e.g, vscode, sublime)

    ### 3.2 Cloning the Repository
        Open a terminal or command prompt.

        Change to the directory where you want to clone the Helmet repository.

        Execute the following command to clone the repository: git clone <https://github.com/PyJim/helmet.git>


    ### 3.3 Setting up the Environment
        Navigate to the cloned repository's directory:cd helmet

        Create a virtual environment: python3 -m venv venv

        Activate the virtual environment:
        For Windows: venv\Scripts\activate


        For Unix or Linux: source venv/bin/activate
        Install the required dependencies:pip install -r requirements.txt

        Set up the database:
        flask db init
        flask db migrate
        flask db upgrade

        This will initialize, migrate, and upgrade the database.

        Run the app by executing flask run in the terminal. The application will then run on port 5000 of your localhost.

## 4. Usage
    The following section describes how to use the various features of the Helmet web application.

    ### 4.1 Signin and Sign up
        Open a web browser.
        Enter the URL(https://helmet-h6d3.onrender.com/) .
        Click on “Get Started”
        Click on the "Sign up" to create a new account.
        Fill in the required details in the registration form and submit.
        After registration enter your credentials and click "Sign in" to access the application.


    ### 4.2 Add Post
        Sign in to the Helmet application.
        Click on the "+" button besides Post
        Fill in the necessary information, such as the title, description, add image and video link..
        Click on the "save" button to add the post.

    ### 4.3 Add Event
        Sign in to the Helmet application.
        Click on the "+" button besides  event
        Provide details about the event, including the title, date, time, location, and description.
        Click on the "Create Event" button to schedule the event.

    ### 4.4 Register for Event
        Either Signed in  or not to the Helmet application.
        Browse the list of events or use the search feature to find a specific event.
        Click on the event to view its details.
        Click on the "Register" button to sign up for the event.

    ### 4.5 View All Posts
        Sign in to the Helmet application.
        Click on the "Home" link.
        Browse through the list of posts to view their details.

    ### 4.6 View All Events
        Sign in to the Helmet application.
        Click on the "Events" link.
        Browse through the list of events to view their details and registrations.

    ### 4.7 Search for Events
        Sign in to the Helmet application.
        Enter keywords or filters in the search bar located on the homepage.
        Press Enter or click on the search icon.
        The application will display a list of events matching the search criteria.

    ### 4.8 Search for Posts
        Sign in to the Helmet application.
        Enter keywords or filters in the search bar located on the homepage.
        Press Enter or click on the search icon.
        The application will display a list of posts matching the search criteria.

## 5. Conclusion
        Congratulations! You have successfully installed and learned how to use the Helmet Flask web application. Now you can report problems, schedule events, and connect with others in your community. If you encounter any issues or have any feedback, please don't hesitate to reach out to us on team.helmet@gmail.com.


