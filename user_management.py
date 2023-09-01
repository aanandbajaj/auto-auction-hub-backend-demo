from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import random
import string

user_management_bp = Blueprint('user_management', __name__)
bcrypt = Bcrypt()

# MySQL configuration and setup (imported from your main app or a separate config file)

def generate_strong_password(length=6):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_username(first_name,last_name,mysql):
    proposed_username = (first_name.lower() + last_name.lower()).replace(' ', '')
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE username = %s",(proposed_username,))
    count = cur.fetchone()[0]
    cur.close()

    if count == 0:
        return proposed_username
    else:
        return proposed_username + str(count)

def getNameFromDB(user_id, mysql):
    cur = mysql.connection.cursor()

    query = "SELECT first_name, last_name FROM users WHERE id = %s"
    cur.execute(query,(user_id,))

    result = cur.fetchone()
    cur.close()
    if result is None:
        return "",""

    first_name, last_name = result
    return first_name, last_name


@user_management_bp.route('/api/verify_user/<int:user_id>', methods=['POST'])
def verify_user(user_id):
    from app import mysql
    # Logic to verify the user (e.g., change is_verified status in the database)
    # Return success response or error message
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_verified = 1 WHERE id = %s",(user_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'User verified successfully'})

@user_management_bp.route('/api/set_credentials/<int:user_id>', methods=['POST'])
def set_credentials(user_id):
    from app import mysql

    first_name, last_name = getNameFromDB(user_id, mysql)

    generated_username = generate_username(first_name,last_name,mysql)
    generated_password = generate_strong_password()

    #encrypting password using bcrypt
    hashed_password = bcrypt.generate_password_hash(generated_password).decode('utf-8')

    cur = mysql.connection.cursor()

    #adding username and encrypted password into the database
    cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s",(generated_username,hashed_password,user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message':'Credentials set successfully','username':generated_username, 'password':generated_password})

    # Return success response or error message

@user_management_bp.route('/api/upload_government_id/<int:user_id>', methods=['POST'])
def upload_government_id(user_id):
    # Logic to handle government ID file upload and update the government_id_filename field
    # Return success response or error message
    pass

# Additional routes and logic for user management (e.g., send verification emails, etc.)

