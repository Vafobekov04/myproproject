from data.repositories.product_repository import ProductRepository
from data.database import get_connection


class ProductService:
    def __init__(self):
        self.connection = get_connection()
        self.repo = ProductRepository(self.connection)

    def get_products(self):
       return self.repo.get_products()

    def search_products(self, keyword):
        return self.repo.search_products(keyword)

    def filter_by_category(self, category_id):
        return self.repo.filter_by_category(category_id)

    def get_categories(self):
        return self.repo.get_categories()

    def add_category(self, category_name):
        if not category_name or category_name.strip() == "":
            return "Название категории обязательно"
        
        self.repo.add_category(category_name)
        return "OK"

    def delete_category(self, category_id):
        self.repo.delete_category(category_id)
        return "OK"

    def update_category(self, category_id, category_name):
        if not category_name or category_name.strip() == "":
            return "Название категории обязательно"
        
        self.repo.update_category(category_id, category_name)
        return "OK"

    def calculate_status(self, quantity):
        if quantity <= 0:
            return "OutOfStock"
        elif quantity < 5:
            return "LowStock"
        else:
            return "InStock"

    def add_product(self, name, price, quantity, category_id):

        if not name:
            return "Название обязательно"

        if float(price) <= 0:
            return "Цена должна быть > 0"

        if int(quantity) < 0:
            return "Количество не может быть отрицательным"

        status = self.calculate_status(quantity)

        self.repo.add_product(name, price, quantity, category_id, status)

        return "OK"

    def update_product(self, product_id, name, price, quantity, category_id):

        status = self.calculate_status(quantity)

        self.repo.update_product(product_id, name, price, quantity, category_id, status)

        return "OK"

    def delete_product(self, product_id):

        self.repo.delete_product(product_id)

        return "OK"