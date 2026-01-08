import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")

db = None
bucket = None

def initialize_firebase():
    """
    Initialize Firebase Admin SDK using service account.
    """
    global db, bucket
    
    if not firebase_admin._apps:
        if FIREBASE_SERVICE_ACCOUNT_PATH and os.path.exists(FIREBASE_SERVICE_ACCOUNT_PATH):
            cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred, {
                'storageBucket': FIREBASE_STORAGE_BUCKET
            })
            print("Firebase Admin SDK initialized successfully.")
        else:
            print(f"Warning: Firebase service account not found at {FIREBASE_SERVICE_ACCOUNT_PATH}. Firebase features will be disabled.")
            return

    db = firestore.client()
    bucket = storage.bucket()

def get_firestore_db():
    """Get Firestore Database client."""
    if db is None:
        initialize_firebase()
    return db

def get_storage_bucket():
    """Get Firebase Storage bucket."""
    if bucket is None:
        initialize_firebase()
    return bucket
