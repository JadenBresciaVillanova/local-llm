# /backend/test_connection.py
import asyncio
import asyncpg
import os

async def test_postgres():
    """Tests the direct connection to PostgreSQL."""
    print("--- Testing PostgreSQL Connection ---")
    try:
        # We will use the exact credentials from your alembic.ini
        conn = await asyncpg.connect(
            user='postgres',
            password='password',
            database='rag_db',
            host='127.0.0.1',
            port=5432
        )
        print("✅ SUCCESS: PostgreSQL connection is valid.")
        
        # Check if pgvector is enabled
        extension_check = await conn.fetchval("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        if extension_check == 1:
            print("✅ SUCCESS: 'vector' extension is enabled in the database.")
        else:
            print("❌ FAILURE: 'vector' extension is NOT enabled.")

        await conn.close()
    except Exception as e:
        print(f"❌ FAILURE: Could not connect to PostgreSQL.")
        print(f"   Error: {e}")
        print("   Troubleshooting:")
        print("   1. Is the `rag_postgres` container running and healthy? (check `docker ps`)")
        print("   2. Are the user, password, and db_name here *exactly* matching docker-compose.yml?")
        print("-------------------------------------\n")


async def main():
    await test_postgres()


if __name__ == "__main__":
    asyncio.run(main())