#!/usr/bin/env python3
"""
Test script to verify database connection and queries work correctly
"""
from data.database import get_connection
from business.dashboard_service import DashboardService

def test_connection():
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    try:
        conn = get_connection()
        if conn:
            print("✓ Database connection successful!")
        else:
            print("✗ Failed to connect to database")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    
    return True

def test_statistics():
    print("\n" + "=" * 60)
    print("Testing Dashboard Statistics")
    print("=" * 60)
    
    try:
        dashboard = DashboardService()
        stats = dashboard.get_statistics()
        
        print(f"✓ Clients: {stats['clients']}")
        print(f"✓ Products: {stats['products']}")
        print(f"✓ Orders: {stats['orders']}")
        print(f"✓ Total Revenue: {stats['total']} ₽")
        
        return True
    except Exception as e:
        print(f"✗ Error fetching statistics: {e}")
        return False

def test_recent_orders():
    print("\n" + "=" * 60)
    print("Testing Recent Orders Query")
    print("=" * 60)
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                o.order_id, 
                c.full_name, 
                o.total_amount, 
                o.status, 
                o.order_date
            FROM Orders o
            LEFT JOIN Clients c ON o.client_id = c.client_id
            ORDER BY o.order_date DESC
            LIMIT 5
        """)
        
        orders = cursor.fetchall()
        
        if orders:
            print(f"✓ Found {len(orders)} recent orders:")
            print()
            for order in orders:
                print(f"  Order #{order['order_id']}")
                print(f"    Client: {order['full_name']}")
                print(f"    Amount: {order['total_amount']} ₽")
                print(f"    Status: {order['status']}")
                print(f"    Date: {order['order_date']}")
                print()
        else:
            print("⚠ No orders found in database")
        
        return True
    except Exception as e:
        print(f"✗ Error fetching orders: {e}")
        return False

if __name__ == "__main__":
    all_passed = True
    
    all_passed = test_connection() and all_passed
    all_passed = test_statistics() and all_passed
    all_passed = test_recent_orders() and all_passed
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)
