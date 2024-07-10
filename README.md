Description
This project is a web-based Student Management System built using Flask and SQLAlchemy. It allows administrators to register, login, add, update, and delete student records.

Features
Authentication: Register and login securely using bcrypt for password hashing.
CRUD Operations: Add, update, and delete student records.
Session Management: Uses Flask sessions to manage user authentication.
Database: SQLite database for data persistence.

Installation
1. Clone the repository:  
git clone https://github.com/priyal1015/student-management-system.git
cd student-management-system

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
pip install -r requirements.txt

4. Initialize the database:
python app.py

5. Run the application:
flask run

Usage
Access the application through your web browser at http://localhost:5000.
Register an account to login and manage student records.
Use the dashboard to view, add, update, or delete student details.
