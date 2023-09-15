To verify user use the following in command prompt:
curl -X POST http://localhost:5000/api/verify_user/userID

How the hashing process works:
User Provides Password:
The user enters their password in the login form.

Retrieving Hashed Password from the Database:
The system retrieves the hashed password associated with the user's account from the database. This hashed password was generated and stored when the user initially set or changed their password.

Hashing the Provided Password:
The system takes the plain text password provided by the user and hashes it using the same cryptographic hash function that was used to hash the original password during storage. This generates a hash value for the provided password.

Comparing Hashes:
The system compares the hash value generated from the provided password with the hash value stored in the database for that user.

If the hash values match, it means the provided password is correct. The user is authenticated and granted access.
If the hash values don't match, it means the provided password is incorrect. The user's access is denied.

How to set credentials using command prompt:
curl -X POST http://localhost:5000/api/set_credentials/<user_id>

How to upload csv auctions to sql:
curl -X POST http://localhost:5000/api/import_auctions

#Site credentials (testing)
Email: aanand222@gmail.com
Username: aanandbajaj
Password: 500

#Site credentials 2 (testing)
    {"message":"Credentials set successfully","password":"Arw{<V","username":"jackchan"}