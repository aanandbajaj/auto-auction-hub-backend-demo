from flask import Blueprint, jsonify, request, make_response
from flask_mysqldb import MySQL
import os

from config import TABLE_NAMES

bidding_bp = Blueprint('bidding', __name__)
table_name = TABLE_NAMES['BIDS_TABLE']


@bidding_bp.route('/api/submit_bid', methods=['POST'])
def submit_bid():
    from app import mysql

    # if no bids for this listing (null), continue
    # if bids for this listing, then find all bids and get max bid

    try:
        data = request.get_json()

        # Get data from JSON
        listing_id = data.get('listing_id')
        user_id = data.get('user_id')
        bid_amount = data.get('bid_amount')

        cursor = mysql.connection.cursor()

        query = "SELECT MAX(amount) FROM bids WHERE listing_id = %s"
        cursor.execute(query, (listing_id,))
        max_bid = cursor.fetchone()["MAX(amount)"]

        if max_bid is None or bid_amount > max_bid:
            # bid amount valid
            query = "INSERT INTO bids (listing_id, user_id, amount) VALUES (%s, %s, %s)"
            cursor.execute(query, (listing_id, user_id, bid_amount))
            mysql.connection.commit()
            cursor.close()
            response = jsonify({'message': 'Bid submitted successfully'})
        else:
            response = jsonify({'error': 'Bid must be larger than the current maximum bid.'}), 400

    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    return response

@bidding_bp.route('/api/get_max_bid/<int:listing_id>', methods=['GET'])
def get_max_bid(listing_id):
    from app import mysql

    try:
        cursor = mysql.connection.cursor()
        query = "SELECT MAX(amount) FROM bids WHERE listing_id = %s"
        cursor.execute(query, (listing_id,))
        max_bid = cursor.fetchone()["MAX(amount)"]
        cursor.close()

        response = jsonify({'max_bid': max_bid})

    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    return response


@bidding_bp.route('/api/get_recent_user_bid/<int:listing_id>/<int:user_id>', methods=['GET'])
def get_recent_user_bid(listing_id, user_id):
    from app import mysql

    try:
        cursor = mysql.connection.cursor()

        # Check if the user has submitted any bids for the listing
        query_check_bid = f"SELECT amount FROM {table_name} WHERE listing_id = %s AND user_id = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(query_check_bid, (listing_id, user_id))
        user_bid = cursor.fetchone()

        response = jsonify({'recent_bid': user_bid})
    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    cursor.close()
    return response


@bidding_bp.route('/api/get_user_bid_listings/<int:user_id>', methods=['GET'])
def get_user_bid_listings(user_id):
    from app import mysql

    print("Received user ID:", user_id)  # Debug print

    try:
        cursor = mysql.connection.cursor()

        query = """
            SELECT
                al.listingCode,
                al.make,
                al.model,
                al.year,
                al.color,
                al.odometer,
                b.amount AS bid_amount,
                a.towing_company,
                al.auction_id
            FROM
                auction_listings al
            INNER JOIN
                bids b ON al.listingCode = b.listing_id
            INNER JOIN
                auctions a ON al.auction_id = a.id
            WHERE
                b.user_id = %s
        """

        cursor.execute(query, (user_id,))
        bid_listings = cursor.fetchall()

        response = jsonify({'bid_listings': bid_listings})

    except Exception as e:
        response = jsonify({'error': str(e)}), 500

    return response


