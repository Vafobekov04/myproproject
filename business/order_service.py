from data.database import get_connection
from data.repositories.order_repository import OrderRepository


class OrderService:

    def __init__(self):
        self.connection = get_connection()
        self.repo = OrderRepository(self.connection)

    def get_orders(self):
        return self.repo.get_all()

    def add_order(self, client_id, employee_id, total_amount, status):
        self.repo.add(client_id, employee_id, total_amount, status)
        return "OK"

    def delete_order(self, order_id):
        self.repo.delete(order_id)

    def get_order_items_text(self, order_id):
        """Get order items as formatted text"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    COUNT(*) as item_count,
                    SUM(quantity) as total_qty
                FROM OrderItems
                WHERE order_id = %s
            """, (order_id,))
            
            result = cursor.fetchone()
            
            if result and result['item_count'] > 0:
                item_count = result['item_count']
                total_qty = result['total_qty'] or 0
                return f"{item_count} позиций ({total_qty} шт)"
            else:
                return "Нет товаров"
        except Exception as e:
            print(f"Error getting order items: {e}")
            return "—"