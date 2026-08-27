from data.repositories.client_repository import ClientRepository
from data.database import get_connection

class ClientService:

    def __init__(self):
        self.repo = ClientRepository(get_connection())

    def get_clients(self):
        return self.repo.get_all()

    def search_clients(self, keyword):
        return self.repo.search(keyword)

    def add_client(self, full_name, phone, email, address):

        if not full_name or not phone:
            return "Ошибка: ФИО и телефон обязательны"

        if "@" in email or email == "":
            self.repo.add(full_name, phone, email, address)
            return "OK"

        return "Ошибка: некорректный email"

    def update_client(self, client_id, full_name, phone, email, address):
        self.repo.update(client_id, full_name, phone, email, address)
        return "OK"

    def delete_client(self, client_id):
        self.repo.delete(client_id)
        return "OK"