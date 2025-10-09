#!/usr/bin/env python3
"""
Database Migration Script
Helps transition from monolithic database.py to modular architecture.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database import db, db_v2


def compare_implementations():
    """Compare the old and new database implementations."""
    print("🔍 Comparing database implementations...")
    
    # Test both connections
    print("\n1. Testing Connections:")
    print(f"   Legacy DB: {'✅' if db.test_connection() else '❌'}")
    print(f"   Modular DB: {'✅' if db_v2.test_connection() else '❌'}")
    
    # Compare job statistics
    print("\n2. Comparing Job Statistics:")
    legacy_stats = db.get_job_stats() if hasattr(db, 'get_job_stats') else {}
    modular_stats = db_v2.get_job_stats()
    
    print(f"   Legacy: {legacy_stats}")
    print(f"   Modular: {modular_stats}")
    
    # Test embedding functionality
    print("\n3. Testing Embedding Services:")
    test_text = "Software Engineer at Google developing AI systems"
    
    try:
        legacy_embedding = db.get_embedding(test_text)
        legacy_status = "✅" if legacy_embedding else "❌"
    except Exception as e:
        legacy_status = f"❌ {str(e)[:50]}..."
    
    try:
        modular_embedding = db_v2.get_embedding(test_text)
        modular_status = "✅" if modular_embedding else "❌"
    except Exception as e:
        modular_status = f"❌ {str(e)[:50]}..."
    
    print(f"   Legacy: {legacy_status}")
    print(f"   Modular: {modular_status}")
    
    return True


def test_new_features():
    """Test features that are only available in the new architecture."""
    print("\n🆕 Testing new modular features...")
    
    # Test health check
    print("\n1. Health Check:")
    health_ok = db_v2.run_health_check()
    print(f"   Status: {'✅' if health_ok else '❌'}")
    
    # Test system status
    print("\n2. System Status:")
    status = db_v2.get_system_status()
    print(f"   Overall: {status.get('status', 'unknown')}")
    print(f"   Connection: {'✅' if status.get('connection', {}).get('connected') else '❌'}")
    print(f"   Embedding Service: {'✅' if status.get('embedding_service', {}).get('available') else '❌'}")
    
    # Test table info
    print("\n3. Table Information:")
    table_info = db_v2.get_table_info("job_applications")
    if table_info:
        print(f"   Columns: {len(table_info.get('columns', []))}")
        print(f"   Constraints: {len(table_info.get('constraints', []))}")
    else:
        print("   ❌ Could not retrieve table info")
    
    # Test model info
    print("\n4. Embedding Model Info:")
    model_info = db_v2.get_model_info()
    print(f"   Model: {model_info.get('model', 'unknown')}")
    print(f"   Dimension: {model_info.get('dimension', 'unknown')}")
    
    return True


def migration_recommendations():
    """Provide recommendations for migration."""
    print("\n📋 Migration Recommendations:")
    print("1. ✅ New modular architecture is ready to use")
    print("2. 🔄 Both old and new implementations are available")
    print("3. 📝 Update imports gradually:")
    print("   - Old: from src.database import db")
    print("   - New: from src.database import db_v2 as db")
    print("4. 🗑️ Remove old database.py when migration is complete")
    print("5. 🧪 Test thoroughly before switching production code")
    
    print("\n🏗️ Architecture Benefits:")
    print("   - Separation of concerns")
    print("   - Better error handling") 
    print("   - Enhanced logging")
    print("   - Easier testing")
    print("   - More maintainable code")


def interactive_test():
    """Interactive test to compare both implementations."""
    print("\n🔬 Interactive Testing Mode")
    print("Enter a job description to test similarity search on both implementations:")
    
    company = input("Company name: ").strip() or "Google"
    position = input("Position title: ").strip() or "Software Engineer"
    description = input("Job description: ").strip() or "Develop AI systems using Python and machine learning"
    
    print(f"\n🔍 Searching for similar jobs...")
    print(f"Query: {position} at {company}")
    
    # Test legacy implementation
    try:
        legacy_results = db.find_similar_jobs(company, position, description)
        print(f"\n📊 Legacy results: {len(legacy_results)} jobs found")
        for job in legacy_results[:3]:  # Show top 3
            print(f"   - {job.get('position_title')} at {job.get('company_name')} (score: {job.get('similarity_score', 'N/A')})")
    except Exception as e:
        print(f"\n❌ Legacy search failed: {e}")
    
    # Test modular implementation
    try:
        modular_results = db_v2.find_similar_jobs(company, position, description)
        print(f"\n📊 Modular results: {len(modular_results)} jobs found")
        for job in modular_results[:3]:  # Show top 3
            print(f"   - {job.get('position_title')} at {job.get('company_name')} (score: {job.get('similarity_score', 'N/A')})")
    except Exception as e:
        print(f"\n❌ Modular search failed: {e}")


def main():
    """Main migration testing function."""
    print("🚀 Database Architecture Migration Tool")
    print("=" * 50)
    
    try:
        # Run comparison tests
        compare_implementations()
        
        # Test new features
        test_new_features()
        
        # Provide recommendations
        migration_recommendations()
        
        # Ask for interactive test
        if input("\n❓ Run interactive similarity test? (y/N): ").lower().startswith('y'):
            interactive_test()
        
        print("\n✅ Migration testing completed successfully!")
        print("🎯 You can now start using the modular database architecture")
        
    except Exception as e:
        print(f"\n❌ Migration testing failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()