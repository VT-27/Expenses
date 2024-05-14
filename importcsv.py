import csv
import sqlite3

# Connecting to the expenses database
conn = sqlite3.connect("expenses.db")

# Creating a cursor object to execute
cur = conn.cursor()

# Create the expenses table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                amount REAL,
                description TEXT,
                date TEXT,
                category TEXT
              )''')

# Open CSV file and reset file pointer
with open('/Users/vivek/Desktop/Learning/FlaskProject/FlaskLearning/expenses.csv', 'r', newline='') as file:
    content = csv.reader(file)

    # Skip header if exists
    next(content, None)

    insert_records = "INSERT INTO expenses (amount, description, date, category) VALUES(?, ?, ?, ?)"

    try:
        cur.executemany(insert_records, content)
        conn.commit()
        print("Data imported successfully!")
    except Exception as e:
        print("Error:", e)
        conn.rollback()

# Close database connection
conn.close()
