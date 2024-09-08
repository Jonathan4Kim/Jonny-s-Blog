# Flask Blog Application

This Flask application allows users to create, edit, view, and manage articles. It includes user authentication, session management, and basic CRUD operations for articles.

## Features
- **User Authentication**: Register, login, and logout functionality.
- **Article Management**: Users can create, edit, view, and delete their articles.
- **Session Management**: User sessions are maintained using Flask's session management.
- **Database Integration**: Utilizes SQLAlchemy with SQLite for database management.

## Prerequisites
- Python 3.x
- Flask
- Flask SQLAlchemy
- Flask Login

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jonathan4Kim/Jonny-s-Blog.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Jonny-s-Blog
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```bash
   python -c "from app import db; db.create_all()"
   ```
5. Run the Flask application:
   ```bash
   python app.py
   ```

## Project Structure

- **app.py**: The main Flask application file containing routes and logic.
- **templates/**: Directory containing HTML templates for the application.
  - `home.html`: Homepage template.
  - `login.html`: Login page template.
  - `register.html`: Registration page template.
  - `create_article.html`: Template for creating a new article.
  - `all_articles.html`: Template for displaying all articles.
  - `display_article.html`: Template for displaying a specific article.
  - `edit_article.html`: Template for editing an article.

## Routes

- **Home** (`/`): Displays the homepage.
- **Login** (`/login`): Allows users to log in.
- **Register** (`/register`): Allows users to create a new account.
- **Create Article** (`/create`): Enables logged-in users to create a new article.
- **View Past Articles** (`/past_articles`): Displays all articles created by the logged-in user.
- **View Article** (`/see-article/<article_name>`): Displays a specific article.
- **Edit Article** (`/edit_article`): Allows users to edit an existing article.
- **Submit Article Edit** (`/submit_edit`): Submits the edits made to an article.
- **Sign Out** (`/signout`): Logs the user out of the session.

## Helper Functions

- **`create_unique_id(email)`**: Generates a unique ID based on the user's email.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author

[Jonathan Kim](https://github.com/Jonathan4Kim)
