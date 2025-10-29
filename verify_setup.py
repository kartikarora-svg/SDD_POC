"""
Setup verification script for Finalytics
Run this after installing dependencies to verify everything is configured correctly
"""
import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('redis', 'Redis'),
        ('langchain', 'LangChain'),
        ('groq', 'Groq'),
        ('yfinance', 'yfinance'),
        ('feedparser', 'feedparser'),
    ]
    
    failed = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name}: {e}")
            failed.append(name)
    
    if failed:
        print(f"\n✗ Failed to import: {', '.join(failed)}")
        print("  Run: pip install -r requirements.txt")
        return False
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        from app.config import settings
        print(f"  ✓ Configuration loaded")
        print(f"    App Name: {settings.APP_NAME}")
        print(f"    Database: {settings.DATABASE_URL}")
        print(f"    Redis: {settings.REDIS_URL}")
        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from app.database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("  ✓ Database connection successful")
            return True
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        print("    Make sure PostgreSQL is running")
        print("    Run: docker-compose up -d postgres")
        return False

def test_redis():
    """Test Redis connection"""
    print("\nTesting Redis connection...")
    try:
        from app.redis_client import redis_client
        redis_client.ping()
        print("  ✓ Redis connection successful")
        return True
    except Exception as e:
        print(f"  ✗ Redis connection failed: {e}")
        print("    Make sure Redis is running")
        print("    Run: docker-compose up -d redis")
        return False

def test_fastapi():
    """Test FastAPI application"""
    print("\nTesting FastAPI application...")
    try:
        from app.main import app
        print(f"  ✓ FastAPI app created")
        print(f"    Title: {app.title}")
        print(f"    Version: {app.version}")
        return True
    except Exception as e:
        print(f"  ✗ FastAPI error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("Finalytics Setup Verification")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_database,
        test_redis,
        test_fastapi,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL TESTS PASSED - Setup is complete!")
        print("\nNext steps:")
        print("  1. Run database migrations: alembic upgrade head")
        print("  2. Start the server: python -m app.main")
        print("  3. Visit: http://localhost:8000")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Please fix the issues above")
        sys.exit(1)

if __name__ == "__main__":
    main()

