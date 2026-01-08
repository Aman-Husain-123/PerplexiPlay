from backend.core.firebase import get_firestore_db, get_storage_bucket
from typing import Dict, Any, Optional

class FirebaseService:
    @staticmethod
    def save_document(collection: str, doc_id: str, data: Dict[str, Any]):
        """Save a document to a Firestore collection."""
        db = get_firestore_db()
        if db:
            db.collection(collection).document(doc_id).set(data)
            return True
        return False

    @staticmethod
    def get_document(collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document from a Firestore collection."""
        db = get_firestore_db()
        if db:
            doc = db.collection(collection).document(doc_id).get()
            if doc.exists:
                return doc.to_dict()
        return None

    @staticmethod
    def upload_file(file_path: str, destination_path: str):
        """Upload a file to Firebase Storage."""
        bucket = get_storage_bucket()
        if bucket:
            blob = bucket.blob(destination_path)
            blob.upload_from_filename(file_path)
            return blob.public_url
        return None
