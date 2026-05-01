# Flask-Blog
A full-featured Flask blog web application with user authentication, profile management, password reset, post creation, and modular architecture using Blueprints.

## Features:
- User Registration & Login
- Password Reset via Email
- Profile Picture Upload
- Create / Update / Delete Posts
- Pagination
- Blueprint Architecture
- Application Factory Pattern

## Installation

### 1. Install project dependencies

This project requires several Python packages to run properly.

To install all required dependencies, use:

```bash
pip install -r requirements.txt
```

## Environment Variables Setup

This project uses environment variables to keep sensitive data secure (such as database credentials and email configuration).

### 2. Create your .env file

A template file named .env.example is provided in the project.
Copy it and rename it to .env:

```bash
cp .env.example .env
```
Then fill in your own configuration values:

```text
EMAIL_USER=your_email_here 
EMAIL_PASS=your_password_here
SECRET_KEY=your_secret_key_here
DATABASE_USER=your_database_user
DATABASE_PASS=your_database_password
```
