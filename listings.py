from flask import Blueprint, jsonify, request, make_response
from flask_mysqldb import MySQL
import os

from config import TABLE_NAMES

listings_bp = Blueprint('listings', __name__)
LISTINGS_CSV_PATH = r'C:\Users\aanan\Documents\Projects\Auto Auction Hub\auto-auction-hub\src\assets\listings.csv'
table_name = TABLE_NAMES['LISTING_TABLE']


# MySQL configuration and setup
@listings_bp.route('/api/import_listings',methods=['POST','OPTIONS'])
def import_listings():
    from app import mysql
    from csv_utils import upload_csv
    upload_csv(mysql, LISTINGS_CSV_PATH, table_name)
    return jsonify({'message': 'Auctions imported successfully'})

# Local code - commented out
# @listings_bp.route('/api/count_listing_images/<int:listing_id>',methods=['GET'])
# def get_num_of_images_by_listing_id(listing_id):
#     images_folder = r'C:\Users\aanan\Documents\Projects\Auto Auction Hub\auto-auction-hub\src\assets\images\Cars'
#     image_links = []
#
#     image_count = 0
#     for filename in os.listdir(images_folder):
#         if filename.startswith(str(listing_id) + '_') and filename.endswith('.jpg'):
#             image_count = image_count + 1
#             image_links.append(os.path.join(images_folder, filename))  # Corrected this line
#
#     response_data = {
#         'image_count': image_count,
#         'image_links': image_links
#     }
#
#     response = jsonify(response_data)
#     return response

@listings_bp.route('/api/count_listing_images/<int:listing_id>',methods=['GET'])
def get_num_of_images_by_listing_id(listing_id):
    from firebase_utils import bucket

    image_count = 0
    image_links = []

    blobs = bucket.list_blobs(prefix=f"{listing_id}_")
    for blob in blobs:
        image_count +=1
        image_links.append(blob.public_url)

    response_data = {
        'image_count':image_count,
        'image_links':image_links
    }

    return response_data

@listings_bp.route('/api/get_listing_by_id/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    from app import mysql

    try:
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE listingCode = %s"
        cursor.execute(query, (listing_id,))
        listing = cursor.fetchall()

        response = jsonify({'listing': listing})
    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    return response


@listings_bp.route('/api/listings/<int:auction_id>', methods=['GET'])
def get_listing_by_auction_id(auction_id):
    from app import mysql

    try:
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE auction_id = %s"
        cursor.execute(query, (auction_id,))
        listings = cursor.fetchall()

        response = jsonify({'listings': listings})
    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    return response


@listings_bp.route('/api/count_listings_by_auction/<int:auction_id>', methods=['GET'])
def count_listings_by_auction(auction_id):
    from app import mysql

    try:
        cursor = mysql.connection.cursor()
        query = f"SELECT COUNT(*) FROM {table_name} WHERE auction_id = %s"
        cursor.execute(query, (auction_id,))
        count = cursor.fetchone()["COUNT(*)"]
        cursor.close()

        response = jsonify({'count': count})
    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    return response