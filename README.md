# Auto Auction Hub Backend

Auto Auction Hub Backend is a Flask-based API that powers the Auto Auction Hub application, providing various functionalities for auctions, bidding, contact forms, listing management, and user management.

## Table of Contents

- [Getting Started](#getting-started)
- [Auction Management](#auction-management)
- [Bidding Management](#bidding-management)
- [Contact Form](#contact-form)
- [Firebase Integration](#firebase-integration)
- [Listing Management](#listing-management)
- [User Management](#user-management)
- [Additional Notes](#additional-notes)
- [License](#license)

## Getting Started

This section includes instructions on setting up and running the Auto Auction Hub Backend. Refer to the main Flask application file, `app.py`, for the main application setup.

## Auction Management

- `auctions_bp.py` - Manages routes related to auctions.
  - `/api/import_auctions` - Imports auctions data from a CSV file.
  - `/api/auctions` - Retrieves all auctions.
  - `/api/auctions/<int:auction_id>` - Retrieves an auction by its ID.
  - `/api/get_auction_details_by_listing/<int:listingCode>` - Retrieves auction details by listing code.
  - `/api/update_auction_times` - Updates auction start and end times.

## Bidding Management

- `bidding_bp.py` - Manages routes related to bidding.
  - `/api/submit_bid` - Allows users to submit bids for listings.
  - `/api/get_max_bid/<int:listing_id>` - Retrieves the maximum bid amount for a listing.
  - `/api/get_recent_user_bid/<int:listing_id>/<int:user_id>` - Retrieves the most recent bid submitted by a user for a listing.
  - `/api/get_user_bid_listings/<int:user_id>` - Retrieves listings for which a user has submitted bids.

## Contact Form

- `contact_form_bp.py` - Manages routes related to contact forms.
  - `/api/send_email` - Allows users to send emails via a contact form.
  - Uses the SendGrid API for email sending.

## Firebase Integration

- `firebase_utils.py` - Provides functions for interacting with Firebase Storage.
  - `upload_file`, `download_file`, `delete_file`, `list_files` - Perform operations on Firebase Storage.
  - `upload_car_images_test` - Uploads car images to Firebase Storage.

## Listing Management

- `listings_bp.py` - Manages routes related to listings.
  - `/api/import_listings` - Imports listings from a CSV file.
  - `/api/count_listing_images/<int:listing_id>` - Counts the number of images associated with a listing in Firebase Storage.
  - `/api/get_listing_by_id/<int:listing_id>` - Retrieves a listing by its ID.
  - `/api/listings/<int:auction_id>` - Retrieves listings for a specific auction.
  - `/api/count_listings_by_auction/<int:auction_id>` - Counts the number of listings for a specific auction.

## User Management

- `user_management_bp.py` - Manages routes related to user management.
  - `/api/verify_user/<int:user_id>` - Verifies a user by updating their verification status.
  - `/api/set_credentials/<int:user_id>` - Sets a username and password for a user.
  - `/api/upload_government_id/<int:user_id>` - Handles the upload of a user's government ID (placeholder).

## Additional Notes

This README provides an overview of the various functionalities and routes in the backend code, helping users understand the capabilities and usage of the Auto Auction Hub Backend.

## License

This project is licensed under the MIT License.
