from flask import Blueprint, jsonify
from config import TABLE_NAMES
import random
from datetime import datetime, timedelta

auctions_bp = Blueprint('auctions', __name__)
AUCTIONS_CSV_PATH = r'C:\Users\aanan\Documents\Projects\Auto Auction Hub\auto-auction-hub\src\assets\auctions.csv'
table_name = TABLE_NAMES['AUCTION_TABLE']

# MySQL configuration and setup

@auctions_bp.route('/api/import_auctions', methods=['POST','OPTIONS'])
def import_auctions():
    from app import mysql
    from csv_utils import upload_csv
    upload_csv(mysql,AUCTIONS_CSV_PATH,table_name,date_columns=['time'])
    return jsonify({'message':'Auctions imported successfully'})


@auctions_bp.route('/api/auctions', methods=['GET'])
def get_auctions():
    from app import mysql

    try:
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        auctions = cursor.fetchall()

        if auctions:
            response = jsonify({'auctions': auctions})
        else:
            response = jsonify({'auctions': []})

    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    cursor.close()
    return response


@auctions_bp.route('/api/auctions/<int:auction_id>', methods=['GET'])
def get_auction(auction_id):
    from app import mysql

    try:
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        cursor.execute(query, (auction_id,))
        auction = cursor.fetchone()

        if auction:
            column_names = [desc[0] for desc in cursor.description]
            auction_dict = dict(zip(column_names, auction))
            response = jsonify(auction_dict)
        else:
            response = jsonify({'message': 'Auction not found'}), 404
    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    cursor.close()
    return response


@auctions_bp.route('/api/get_auction_details_by_listing/<int:listingCode>',methods=['GET'])
def get_auction_details_by_listing(listingCode):
    from app import  mysql
    try:
        cursor = mysql.connection.cursor()

        query = """
            SELECT a.*
            FROM auctions AS a
            JOIN auction_listings AS al ON a.id = al.auction_id
            WHERE al.listingCode = %s
        """

        cursor.execute(query,(listingCode,))
        auction_details = cursor.fetchone()


        if auction_details:
            column_names = [desc[0] for desc in cursor.description]
            auction_dict = {column_names[i]: auction_details[i] for i in range(len(column_names))}
            response = jsonify(auction_dict)
        else:
            response = jsonify({'error':'Auction details not found'})
    except Exception as e:
        response = jsonify({'error':str(e)}),500

    cursor.close()
    return response


# Add other routes and logic for auctions
import random
from datetime import datetime, timedelta

# ...

import random
from datetime import datetime, timedelta

# ...

@auctions_bp.route('/api/update_auction_times', methods=['POST'])
def update_auction_times():
    from app import mysql

    try:
        cursor = mysql.connection.cursor()

        # Set the fixed start time to August 31, 2023 at 3:00 PM ET
        fixed_start_time = datetime(2023, 8, 31, 15, 0)

        query = f"SELECT id FROM {table_name}"
        cursor.execute(query)
        auction_ids = [row[0] for row in cursor.fetchall()]

        for auction_id in auction_ids:
            # Calculate the new end_time
            random_days = random.randint(1, 10)
            random_seconds = random.randint(0, 86399)  # 0 to 23:59:59 seconds
            random_interval = timedelta(days=random_days, seconds=random_seconds)
            new_end_time = fixed_start_time + random_interval

            # Update the times in the database
            update_query = f"UPDATE {table_name} SET time = %s, end_time = %s WHERE id = %s"
            cursor.execute(update_query, (fixed_start_time, new_end_time, auction_id))

        # Commit the changes
        mysql.connection.commit()

        response = jsonify({'message': 'Auction times updated successfully'})
    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    cursor.close()
    return response

