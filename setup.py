"""
Setup Script - Initialize MongoDB Database

WHAT: Loads initial dataset into MongoDB Atlas
HOW: Generates dataset using dataset_generator.py and inserts into MongoDB
WHY: One-time setup to populate database with initial training data
"""

from dataset_generator import create_dataset
from database import db_manager


def main():
    """
    Initialize MongoDB database with initial dataset.
    """
    print("🚀 Setting up Phishing Detection Database")
    print("=" * 40)
    
    # Generate dataset
    print("📧 Generating initial dataset...")
    dataset = create_dataset()
    print(f"✅ Generated {len(dataset)} email samples")
    
    # Connect to MongoDB
    print("\n🗄️  Connecting to MongoDB Atlas...")
    if not db_manager.connect():
        print("❌ Failed to connect to MongoDB. Check your .env file.")
        return
    
    # Check if collection already has data
    existing_count = db_manager.count_documents()
    if existing_count > 0:
        print(f"⚠️  Collection already contains {existing_count} documents")
        response = input("Do you want to clear and reinitialize? (y/n): ").strip().lower()
        if response == 'y':
            db_manager.collection.delete_many({})
            print("✅ Cleared existing documents")
        else:
            print("❌ Setup cancelled")
            db_manager.disconnect()
            return
    
    # Insert dataset
    print("\n📥 Inserting dataset into MongoDB...")
    db_manager.insert_many(dataset)
    
    # Verify insertion
    final_count = db_manager.count_documents()
    phishing_count = db_manager.count_documents({"label": 1})
    legit_count = db_manager.count_documents({"label": 0})
    
    print("\n📊 Database Statistics:")
    print(f"   Total documents: {final_count}")
    print(f"   Phishing emails: {phishing_count}")
    print(f"   Legitimate emails: {legit_count}")
    
    # Disconnect
    db_manager.disconnect()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run analytics: python analytics.py")
    print("2. Train models: python models.py")
    print("3. Add new emails: python update_dataset.py")


if __name__ == "__main__":
    main()
