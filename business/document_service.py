from data.database import get_connection
from data.repositories.document_repository import DocumentRepository
from utils.pdf_generator import PDFGenerator
from utils.order_document_generator import OrderDocumentGenerator


class DocumentService:

    def __init__(self):
        self.connection = get_connection()
        self.repo = DocumentRepository(self.connection)
        self.pdf_generator = PDFGenerator()
        self.order_doc_generator = OrderDocumentGenerator()

    def get_documents(self):
        return self.repo.get_all()

    def get_documents_with_client_info(self):
        """Get documents with client information joined from Orders table"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    d.document_id,
                    d.order_id,
                    c.full_name as client_name,
                    d.document_type,
                    d.create_date,
                    d.file_path
                FROM Documents d
                LEFT JOIN Orders o ON d.order_id = o.order_id
                LEFT JOIN Clients c ON o.client_id = c.client_id
                ORDER BY d.create_date DESC
            """)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error fetching documents with client info: {e}")
            return []

    def get_order_data(self, order_id):
        """Get order data for PDF generation"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    o.order_id,
                    o.total_amount,
                    o.order_date,
                    o.status
                FROM Orders o
                WHERE o.order_id = %s
            """, (order_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error fetching order data: {e}")
            return None

    def get_client_data(self, order_id):
        """Get client data for PDF generation"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    c.client_id,
                    c.full_name,
                    c.email,
                    c.phone,
                    c.address
                FROM Clients c
                JOIN Orders o ON c.client_id = o.client_id
                WHERE o.order_id = %s
            """, (order_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error fetching client data: {e}")
            return None

    def get_order_items(self, order_id):
        """Get all order items with product details"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    oi.order_item_id,
                    oi.product_id,
                    p.product_name,
                    c.category_name,
                    oi.quantity,
                    oi.price,
                    oi.subtotal
                FROM OrderItems oi
                JOIN Products p ON oi.product_id = p.product_id
                LEFT JOIN Categories c ON p.category_id = c.category_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
            """, (order_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error fetching order items: {e}")
            return []

    def get_employee_data(self, employee_id):
        """Get employee data"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT full_name FROM Employees WHERE employee_id = %s
            """, (employee_id,))
            result = cursor.fetchone()
            cursor.close()
            return result.get('full_name', '') if result else ''
        except Exception as e:
            print(f"Error fetching employee data: {e}")
            return ''
    
    def get_payment_info(self, order_id):
        """Get payment information for order"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    payment_method,
                    payment_date,
                    status
                FROM Payments
                WHERE order_id = %s
                LIMIT 1
            """, (order_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return {
                    'method': result.get('payment_method', 'Не указано'),
                    'date': result.get('payment_date', ''),
                    'status': self._translate_payment_status(result.get('status', 'Pending'))
                }
            return None
        except Exception as e:
            print(f"Error fetching payment info: {e}")
            return None
    
    def _translate_payment_status(self, status):
        """Translate payment status"""
        statuses = {
            'Pending': 'Ожидает оплаты',
            'Paid': 'Оплачено',
            'Failed': 'Ошибка при оплате'
        }
        return statuses.get(status, status)
    
    def get_delivery_info(self, order_id):
        """Get delivery information for order"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    delivery_method,
                    delivery_address,
                    delivery_date
                FROM Orders
                WHERE order_id = %s
            """, (order_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return {
                    'method': result.get('delivery_method') or 'Не указано',
                    'address': result.get('delivery_address') or '',
                    'date': result.get('delivery_date') or ''
                }
            return None
        except Exception as e:
            print(f"Error fetching delivery info: {e}")
            return None

    def add_document(self, order_id, document_type):
        """Add new document with PDF generation"""
        try:
            # Get order and client data
            order_data = self.get_order_data(order_id)
            client_data = self.get_client_data(order_id)
            order_items = self.get_order_items(order_id)
            
            if not order_data or not client_data:
                return "Ошибка: Не удалось получить данные заказа или клиента"
            
            # Get employee name from order
            employee_name = ""
            try:
                cursor = self.connection.cursor(dictionary=True)
                cursor.execute("SELECT employee_id FROM Orders WHERE order_id = %s", (order_id,))
                order = cursor.fetchone()
                cursor.close()
                if order and order.get('employee_id'):
                    employee_name = self.get_employee_data(order.get('employee_id'))
            except:
                pass
            
            # Generate professional order document
            if document_type.lower() == 'order':
                payment_info = self.get_payment_info(order_id)
                delivery_info = self.get_delivery_info(order_id)
                
                file_path = self.order_doc_generator.generate_order_document(
                    order_data,
                    client_data,
                    order_items,
                    employee_name,
                    payment_info,
                    delivery_info,
                    notes=""
                )
            else:
                # Use old PDF generator for other document types
                file_path = self.pdf_generator.generate_pdf(
                    document_type, 
                    order_data, 
                    client_data, 
                    order_items, 
                    employee_name
                )
            
            # Save to database
            self.repo.add(order_id, document_type, file_path)
            return "OK"
        except Exception as e:
            return f"Ошибка при создании документа: {str(e)}"

    def delete_document(self, document_id):
        self.repo.delete(document_id)