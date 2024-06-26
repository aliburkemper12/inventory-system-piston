# inventory-system
Inventory system for the IT department.

Created over a course of four weeks during a summer internship. (Due to company protocol, never used by any one other then myself).

# Tech Stack

Front end:
- JS/HTML/CSS
- Jinja2
  
Back end:
- Flask
- Python

Databases:
- SQLite/SQLAlchemy

Libraries:
- AJAX
- Werkzeug.security

Deployed using Waitress. Follows CRUD fundamental operations.


# Features

This web application allows IT employees to view, edit, add, and delete items from a database. The item database uses SQLite. '

Search feature.

View items in a specific location.

Users can also sort the data table by ascending or descending values by column.

Displays items that have a low quantity in red and displays the number of alerts at the top of the page. (Quantity alert number is changed by the user and is unique to every item).

'Partial' tab with simplified table where user can choose an item and increment its quantity by an integer. Useful when receiving shipments.

User tab that allows user to change username or password.

There is a login page that requires a username and password. Only the admin account can add or delete users.
All passwords are hashed and salted using werkzeug.security and stored in a SQL table.
All views besides the login are protected, and admin only pages require the admin role to view.

Deployed locally for the IT deparment to keep track of inventory, including labels which are used everyday and are a critical part of production.

# What I Learned

This project was created using Python-Flask and grew my knowledge with the framework. 
During the creation of this project I gained profiency in SQL.
I had many issues related to front-end development that required me to troubleshoot, debug, and consult the documentation for various frameworks.

Examples:

Login page

![Login page](src/static/login_snip.png)

Home page

![Home page](src/static/home_snip.png)

Increment page

![Increment page](src/static/partial_snip.png)

Add item page

![Add page](src/static/add_snip.png)

Edit item page

![Edit page](src/static/edit_snip.png)

User page

![User page](src/static/user_snip.png)

Admin page

![Admin page](src/static/admin_snip.png)

