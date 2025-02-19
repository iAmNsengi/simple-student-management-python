## Steps to consider while running the app

1. Create a virtual environment

    `python -m venv venv`

3. Activate the virtual environment

    `source venv/Scripts/activate` (on windows)
   `source venv/bin/activate` (on linux based OS or MacOs)

4. Install packages

   `pip install -r requirements.txt`

5. Run the app

   `python app.py`

6. Create a .env file in the same dir add a key API_KEY

`API_KEY= your-api-key-here-generated-from-a-uuid-generator-for-safety`




## FYI: Make sure you have an XAMPP server running sql, and you have a database there called `student_db`
