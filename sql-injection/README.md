# Sql-Injection

# Breif Overview

In this lab we are experimenting with sql injection into a flask app using sqlite as the database.

# Folder files

bugapp.py -> App with Vulnerability
database.db -> Database for Name and Email
fixedapp.py -> App with Vulnerability Patch

# Setup Instructions for bugapp.py

1. Pull the repo to your local computer
2. cd into ./sql-injection
3. Create a virtual environment run python -m venv venv
4. Activate the environment run venv\Scripts\activate
5. Install flask run pip install flask
6. Start the vulnerable app run python bugapp.py
7. Open another new terminal to write the following commands
8. Check to see that nothing is in the database run curl -X GET "http://127.0.0.1:5000/users"
9. Add user 1. Send a POST request to the ./add-user API run curl -X POST "http://127.0.0.1:5000/add_user" -H "Content-Type: application/json" -d '{\"name\": \"zane\", \"email\": \"
zanesole@hotmail.com\"}'
10. Add user 2. Send a POST request to the ./add-user API run curl -X POST "http://127.0.0.1:5000/add_user" -H "Content-Type: application/json" -d '{\"name\": \"ashley\", \"email\": \"
ashleypender@hotmail.com\"}'
11. Search for a user called zane run curl -X GET "http://127.0.0.1:5000/search?q=zane"
12. Now exploit with a sql injection run curl -X GET "http://127.0.0.1:5000/search?q='OR'1'='1"

# Setup Instructions for fixedapp.py

1. cd into ./sql-injection
2. Start the vulnerable app run python bugapp.py
3. Open another new terminal to write the following commands
4. Check to see that users we added are in the database run curl -X GET "http://127.0.0.1:5000/users"
5. Search for a user called ashley run curl -X GET "http://127.0.0.1:5000/search?q=ashley"
6. Try the exploit again which won't work run curl -X GET "http://127.0.0.1:5000/search?q='OR'1'='1"

# Software and libraries Used

Python -> server-side programming language
Flask -> light weight webframework server
Powershell -> to interact with the app
Sqlite3 -> database to have persistant data storage
Requests -> handle responses
jsonify -> converts to json string
curl -> to send http requests from powershell to our flask server

# Vulnerability

The vulnerability is this code: cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{query}%'")

The code snippet is found in the bugapp.py code in the /search route. 

How it works?

It directly concatenates user input from the search query into a Sql query without sanitization.
Sqlite3 will interpret native sql commands as a vaild query. 
This can lead to entire data dumps or even deletion of data. The injection we used was 'OR'1'='1 which results in true and returns all users.

# Mitigation

The patch for the vulnerable code is: cur.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + query + '%',))

The code snippet is found in the fixedapp.py code in the /search route.

How it works ?

The code seperates Sql logic from user input, by using the ? acting as a placeholder (sql bind parameter) anything passed as a query will now be seen as a string to SQlite3 and not a sql command.
