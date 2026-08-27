"""
Migration script to add delivery and payment info columns to Orders and Payments tables
"""
from data.database import get_connection


def migrate():
    """Add missing columns to Orders and Payments tables"""
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Add delivery columns to Orders if they don't exist
        cursor.execute("DESCRIBE Orders")
        columns = [col[0] for col in cursor.fetchall()]
        
        if 'delivery_method' not in columns:
            print("Adding delivery_method column to Orders...")
            cursor.execute("""
                ALTER TABLE Orders
                ADD COLUMN delivery_method VARCHAR(50)
            """)
            print("✓ delivery_method added")
        
        if 'delivery_address' not in columns:
            print("Adding delivery_address column to Orders...")
            cursor.execute("""
                ALTER TABLE Orders
                ADD COLUMN delivery_address VARCHAR(255)
            """)
            print("✓ delivery_address added")
        
        if 'delivery_date' not in columns:
            print("Adding delivery_date column to Orders...")
            cursor.execute("""
                ALTER TABLE Orders
                ADD COLUMN delivery_date DATE
            """)
            print("✓ delivery_date added")
        
        # Try to add columns to Payments table if it exists
        try:
            cursor.execute("DESCRIBE Payments")
            print("✓ Payments table exists")
        except Exception as e:
            print(f"Note: Payments table doesn't exist yet (this is okay)")
        
        connection.commit()
        print("\n✓ Migration completed successfully!")
        
    except Exception as e:
        connection.rollback()
        print(f"Error during migration: {e}")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    migrate()
