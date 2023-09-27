from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


load_dotenv()

# creates an instance of Flask class and assigns it to app variable
# __name__ is a special Python variable that refers to current module
# in this case it will be "__main__" when script is executed as main program
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

from auctions import auctions_bp
from listings import listings_bp
from user_management import user_management_bp
from bidding import bidding_bp
from contact_form import contact_form_bp

# Register the blueprints along with the CORS instances
app.register_blueprint(auctions_bp)
app.register_blueprint(listings_bp)
app.register_blueprint(user_management_bp)
app.register_blueprint(bidding_bp)
app.register_blueprint(contact_form_bp)

bcrypt = Bcrypt()

# upload file configurations
# don't need at the moment because I'm not asking the user for license
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Configure MySQL connection
if os.environ.get('FLASK_ENV') == 'development':
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'ElonMusk$123'
    app.config['MYSQL_DB'] = 'auto_auction_hub_local'
else:
    app.config['MYSQL_HOST'] = os.environ.get('DB_HOST')
    app.config['MYSQL_USER'] = os.environ.get('DB_USER')
    app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASSWORD')
    app.config['MYSQL_DB'] = os.environ.get('DB_NAME')

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return 'Welcome to the Flask backend!'

# decorator
# associates / route of Flask application with 'hello()' function
# @app.route('/') tells Flask that when user accesses the root URl of the application ('/'), the hello() function should be executed
# in Flask, routes are defined using @app.route decorator
# when you use @app.route('/') before function, it associates function with specified route, in this case ('/')
@app.route('/api/login', methods=['POST'])
def login():
    # login logic
    data = request.get_json()

    print(data)
    username = data.get('username')
    password = data.get('password')

    cur = mysql.connection.cursor()
    query = "SELECT id, password FROM users WHERE username = %s"
    cur.execute(query, (username,))
    user_data = cur.fetchone()

    if user_data:
        if isinstance(user_data, dict):  # Check if user_data is a dictionary (JawsDB)
            user_id = user_data['id']
            hashed_password = user_data['password']
        elif isinstance(user_data, tuple):  # Check if user_data is a tuple (MySQL)
            user_id = user_data[0]
            hashed_password = user_data[1]
        else:
            # Handle unsupported data format
            response = jsonify({'message': 'Unsupported data format'}), 500
            return response

        if bcrypt.check_password_hash(hashed_password, password):
            # Password is correct, proceed with login
            # Return success response along with user ID
            response = jsonify({'message': 'Login successful', 'userId': user_id})
        else:
            response = jsonify({'message': 'Invalid credentials'}), 401
    else:
        response = jsonify({'message': 'User not found'}), 404

    cur.close()
    return response



@app.route('/api/signup', methods=['POST'])
def signup():
    # handle signup logic
    data = request.get_json()
    # username/password ommitted because empty until verified
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    address = data.get('homeAddress')
    phone_number = data.get('phoneNumber')

    # government id ommitted because will ask for it in the email followup
    # government_id = request.files['governmentId']

    # store user data in the database
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (username, password, email, first_name, last_name, address, phone_number, is_verified, government_id_filename) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (username, password, email, first_name, last_name, address, phone_number, False, None))  # Initial placeholder for government_id_filename

    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Signup successful'})


if __name__ == '__main__':
    # Use the PORT environment variable if available
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)

