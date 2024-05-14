# Expense Project in Flask

#Imporing necessary modules
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, g, flash, redirect, request, render_template, url_for, session
import secrets # Module for generating cryptographically strong random numbers



# Configure application
app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True # Enable auto-reloading of templates

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def get_db_connection():
    conn = sqlite3.connect('expenses.db') # Establish a connection to the SQLite database 
    conn.row_factory = sqlite3.Row # Set row factory to return rows as dictionaries
    return conn # Return the database connection

# Login Route
@app.route("/", methods = ["GET", "POST"])
def login():
    
    # Get a connection to the database
    conn = get_db_connection()  

    # Get the value of the "name" field from the form
    name = request.form.get("name") 

    # Get the value of the "password" field from the form
    password = request.form.get("password")

    if request.method == "POST":    # Check if the request method is POST
        cur = conn.cursor()         # Create a cursor object
        cur.execute("Select * from users where username = ? and password = ?", (name, password))    # Execute SQL query to fetch user
        user = cur.fetchone()   # Fetch the first row of the result set
        cur.close()
        conn.close()

        if user:    # Check if user exists
            
            # Flash a success message
            flash('Login successful!', 'success')           

            # Redirect to the index route
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')

# Index Page for Expenses
@app.route("/index", methods=["GET", "POST"])
def index():
    # Get a connection to the database
    conn = get_db_connection()

    if request.method == "GET":
        # Fetch all expenses from the database
        expenses = conn.execute('SELECT * FROM expenses order by rowid DESC').fetchall()

        total_row = conn.execute('select sum(amount) from expenses'). fetchone()

        # Get total amount or set it to 0 if it's None
        total = total_row[0] if total_row else 0
        conn.close()

        # Render the index template with expenses and total amount
        return render_template('index.html', expenses=expenses, total=total)
    
    else:

        # Get the value of the "amount, description, date and category" field from the form
        amount = request.form.get("amount")
        description = request.form.get("description")
        date = request.form.get("date")
        category = request.form.get("category")
        
        # Check if any of the fields are empty
        if not all([amount, description, date, category]):
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))
        
        conn.execute("insert into expenses (amount, description, date, category) values (?, ?, ?, ?)", (amount, description, date, category))
        conn.commit()
        flash('Expense added successfully!', 'success')
        conn.close()
        return redirect(url_for('index')) 
    
# Delete Expenses Route
@app.route("/delexpenses", methods= ["POST"])
def delete():
    conn = get_db_connection()
    # Get the value of the "id" field from the form
    id = request.form.get("id")
    if id:
        conn.execute('delete from expenses where id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Search Expenses Route
@app.route("/search")
def search():
    # Get the value of the "query" parameter from the request URL
    q = request.args.get('query')
    conn = get_db_connection()
    if q:
        cursor = conn.cursor()
        # Execute SQL query to search for expenses for all columns
        cursor.execute("Select * from expenses where amount like ? OR description like ? or date like ? OR category like ?  ", ('%' + q + '%','%' + q + '%', '%' + q + '%', '%' + q + '%', ))
        
        # Fetch all the results
        results = cursor.fetchall() 
        conn.close()
        # Render search results as partial HTML response
        return render_template('search.html', results = results)
    else:
        conn.close()
        #return redirect(url_for('index'))
        return render_template('search.html', results=[])

#Edit Route
@app.route('/edit', methods=['POST']) # Define a route for handling POST requests to /edit
def edit():
    conn = get_db_connection()

    # Iterate over form data items
    for key, value in request.form.items(): 
        # Ensure the key follows the expected format
        if '_' in key:  # Check if the key contains an underscore
            expense_id, field = key.split('_', 1)       # Split the key into expense_id and field
            # Update the corresponding expense record
            conn.execute(f'UPDATE expenses SET {field} = ? WHERE id = ?', (value, expense_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)