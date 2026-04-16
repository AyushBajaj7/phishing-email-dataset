"""
MongoDB Database Module

WHAT: Manages MongoDB Atlas connection and operations
HOW: Uses pymongo driver for document-based NoSQL operations
WHY: Email data is semi-structured (nested sender info, features) requiring flexible schema
WHY NOT: Not using SQL because email data doesn't fit rigid table structure; not using graph DB because relationships are not the primary concern
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

# Load environment variables
load_dotenv()


class MongoDBManager:
    """
    Manages MongoDB connection and operations for phishing detection system.
    """
    
    def __init__(self):
        """
        Initialize MongoDB connection using environment variables.
        """
        self.uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("DATABASE_NAME", "phishing_detection")
        self.collection_name = os.getenv("COLLECTION_NAME", "emails")
        
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """
        Establish connection to MongoDB Atlas.
        
        WHAT: Connect to MongoDB cluster
        HOW: pymongo MongoClient with connection string
        WHY: Required for all database operations
        """
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print("✅ Connected to MongoDB Atlas")
            return True
        except errors.ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """
        Close MongoDB connection.
        
        WHAT: Terminate connection to MongoDB
        HOW: client.close()
        WHY: Proper resource cleanup
        """
        if self.client:
            self.client.close()
            print("✅ Disconnected from MongoDB Atlas")
    
    def insert_many(self, documents):
        """
        Insert multiple documents into collection.
        
        WHAT: Bulk insert of email documents
        HOW: collection.insert_many()
        WHY: Efficient for initial dataset population
        """
        try:
            result = self.collection.insert_many(documents)
            print(f"✅ Inserted {len(result.inserted_ids)} documents")
            return result.inserted_ids
        except errors.BulkWriteError as e:
            print(f"❌ Bulk write error: {e}")
            return None
    
    def find(self, query=None, projection=None):
        """
        Find documents matching query.
        
        WHAT: Retrieve documents from collection
        HOW: collection.find() with optional query and projection
        WHY: Required for data retrieval and analysis
        """
        try:
            cursor = self.collection.find(query, projection)
            return list(cursor)
        except errors.PyMongoError as e:
            print(f"❌ Find error: {e}")
            return []
    
    def count_documents(self, query=None):
        """
        Count documents matching query.
        
        WHAT: Get count of documents
        HOW: collection.count_documents()
        WHY: Useful for analytics and validation
        """
        try:
            return self.collection.count_documents(query or {})
        except errors.PyMongoError as e:
            print(f"❌ Count error: {e}")
            return 0
    
    def update_one(self, filter_query, update_data):
        """
        Update a single document.
        
        WHAT: Modify one document matching filter
        HOW: collection.update_one()
        WHY: Required for updating existing email records
        """
        try:
            result = self.collection.update_one(filter_query, update_data)
            print(f"✅ Updated {result.modified_count} document(s)")
            return result.modified_count
        except errors.PyMongoError as e:
            print(f"❌ Update error: {e}")
            return 0
    
    def delete_one(self, filter_query):
        """
        Delete a single document.
        
        WHAT: Remove one document matching filter
        HOW: collection.delete_one()
        WHY: Required for data cleanup
        """
        try:
            result = self.collection.delete_one(filter_query)
            print(f"✅ Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except errors.PyMongoError as e:
            print(f"❌ Delete error: {e}")
            return 0
    
    def check_duplicate(self, raw_email, sender_email):
        """
        Check if email already exists in database.
        
        WHAT: Prevent duplicate entries
        HOW: Query for matching raw_email and sender_email
        WHY: Ensures data integrity and prevents bias from duplicates
        """
        query = {
            "raw_email": raw_email,
            "sender.email": sender_email
        }
        return self.count_documents(query) > 0


# Singleton instance for application-wide use
db_manager = MongoDBManager()
