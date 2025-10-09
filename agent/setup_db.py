#!/usr/bin/env python3
"""
Simple setup script to initialize the Aria database with vector embeddings
"""

from src.database import db

def main():
    print("🚀 Setting up Aria database with vector embeddings...")
    
    # Test connection
    print("1️⃣ Testing database connection...")
    if not db.test_connection():
        print("❌ Cannot connect to database. Please check your .env configuration.")
        return False
    
    # Initialize schema
    print("2️⃣ Initializing database schema...")
    if not db.initialize_schema():
        print("❌ Failed to initialize database schema.")
        return False
    
    # Add unique constraint for existing databases
    print("3️⃣ Adding unique constraint for company_name and position_title...")
    if not db.add_unique_constraint():
        print("⚠️ Warning: Failed to add unique constraint (this is OK if constraint already exists)")
    
    # Backfill embeddings for existing jobs
    print("4️⃣ Generating embeddings for existing jobs...")
    if not db.backfill_embeddings():
        print("⚠️ Warning: Failed to backfill embeddings (this is OK if no existing jobs)")
    
    print("✅ Database setup completed successfully!")
    print("\n📋 Available API endpoints:")
    print("  GET  /api/db/test                - Test database connection")
    print("  POST /api/db/init               - Initialize database schema")
    print("  POST /api/db/add-unique-constraint - Add unique constraint for company+position")
    print("  POST /api/jobs/save             - Save a job application")
    print("  POST /api/jobs/similar          - Find similar job applications (vector embeddings)")
    print("  POST /api/jobs/backfill         - Generate embeddings for existing jobs")
    print("  GET  /api/jobs/all              - Get all job applications")
    print("\n🎯 Example similarity search with vector embeddings:")
    print('  curl -X POST http://localhost:8080/api/jobs/similar \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"company_name": "Google", "position_title": "Software Engineer", "job_description": "Build amazing products...", "threshold": 0.75}\'')
    
    print("\n🧠 Vector Embedding Features:")
    print("  • Semantic understanding (ML Engineer ≈ Data Scientist)")
    print("  • Precise similarity scores (0.0 to 1.0)")
    print("  • Customizable threshold (default: 0.75)")
    print("  • Automatic embedding generation for new jobs")
    print("  • Unique company+position constraint prevents duplicates")
    
    return True

if __name__ == "__main__":
    main()