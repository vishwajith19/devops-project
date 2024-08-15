from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'some-mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'my-secret-pw')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'my_database')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))

mysql = MySQL(app)

def init_mysql():
    try:
        # Connect to MySQL directly to initialize the database
        connection = MySQLdb.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            port=app.config['MYSQL_PORT']
        )
        cursor = connection.cursor()
        
        # Use the specific database
        cursor.execute("CREATE DATABASE IF NOT EXISTS my_database;")
        cursor.execute("USE my_database;")
        
        # Create the 'users' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            );
        """)
        
        # Grant privileges
        cursor.execute("GRANT ALL PRIVILEGES ON my_database.* TO 'your_user'@'%';")
        cursor.execute("FLUSH PRIVILEGES;")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database and table initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

@app.before_first_request
def setup_database():
    # Initialize the database and create the table
    init_mysql()

# Routes for CRUD operations

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    name = data['name']
    email = data['email']
    cursor = mysql.connection.cursor()
    
    # Ensure the correct database is being used
    cursor.execute("USE my_database;")
    
    # Insert the new user
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User created!'}), 201

@app.route('/user', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Ensure the correct database is being used
    cursor.execute("USE my_database;")
    
    # Fetch all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Ensure the correct database is being used
    cursor.execute("USE my_database;")
    
    # Fetch user by id
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.close()
    return jsonify(user), 200

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    cursor = mysql.connection.cursor()
    
    # Ensure the correct database is being used
    cursor.execute("USE my_database;")
    
    # Update the user
    cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User updated!'}), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    cursor = mysql.connection.cursor()
    
    # Ensure the correct database is being used
    cursor.execute("USE my_database;")
    
    # Delete the user
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User deleted!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
