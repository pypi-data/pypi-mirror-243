import os

import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase():
    try:
        # Check if Firebase app is already initialized
        firebase_admin.get_app()
    except ValueError as e:
        # Get the path to the firebase_sa.json file which is in the same directory as this script
        cred_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "firebase_sa.json"
        )
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)


# Test the function
if __name__ == "__main__":
    initialize_firebase()
