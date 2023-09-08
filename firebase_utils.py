import os.path
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore

# Setup Firebase
cred = credentials.Certificate("auto-auction-hub-firebase-adminsdk-ncyzs-fb30176dc5.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'auto-auction-hub.appspot.com'})

# Reference to Firebase Storage client
bucket = storage.bucket()

# Upload a file to Firebase Storage
def upload_file(filename, destination):
    blob = bucket.blob(destination)
    blob.upload_from_filename(filename)

# Download a file from Firebase Storage
def download_file(source, destination):
    blob = bucket.blob(source)
    blob.download_to_filename(destination)

# Delete a file from Firebase Storage
def delete_file(filename):
    blob = bucket.blob(filename)
    blob.delete()

# List files in a Firebase Storage folder
def list_files(folder):
    blobs = bucket.list_blobs(prefix=folder)
    file_list = [blob.name for blob in blobs]
    return file_list

def upload_car_images_test(image_folder, destination_folder):
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg'):
            local_image_path = os.path.join(image_folder, filename)
            remote_image_path = filename

            blob = bucket.blob(remote_image_path)
            blob.upload_from_filename(local_image_path)


upload_car_images_test(
    r'C:\Users\aanan\Documents\Projects\Auto Auction Hub\auto-auction-hub\src\assets\images\Cars',
    'images'
)
