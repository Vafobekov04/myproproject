

from data.database import get_connection
from business.product_service import ProductService

# Перечень категорий бытовой техники
CATEGORIES = [
    "Холодильники и морозильники",
    "Стиральные машины",
    "Посудомоечные машины",
    "Микроволновые печи",
    "Электрические плиты",
    "Газовые плиты",
    "Вытяжки и вентиляция",
    "Кухонные комбайны",
    "Блендеры",
    "Тостеры",
    "Чайники электрические",
    "Кофеварки",
    "Пылесосы",
    "Пароварки",
    "Мультиварки",
    "Электрические духовки",
    "Хлебопечки",
    "Соковыжималки",
    "Увлажнители воздуха",
    "Осушители воздуха",
    "Кондиционеры",
    "Обогреватели",
    "Вентиляторы",
    "Кухонные вытяжки",
    "Посушители для посуды",
    "Проточные фильтры для воды",
    "Варочные панели",
    "Духовые шкафы",
]

def populate_categories():
    """Добавляет категории бытовой техники в базу данных."""
    try:
        service = ProductService()
        
        print("Начало добавления категорий бытовой техники...")
        print(f"Всего категорий для добавления: {len(CATEGORIES)}\n")
        
        added_count = 0
        for i, category_name in enumerate(CATEGORIES, 1):
            try:
                result = service.add_category(category_name)
                if result == "OK":
                    print(f"✓ ({i}/{len(CATEGORIES)}) Добавлена: {category_name}")
                    added_count += 1
                else:
                    print(f"✗ ({i}/{len(CATEGORIES)}) Ошибка: {result}")
            except Exception as e:
                print(f"✗ ({i}/{len(CATEGORIES)}) Ошибка при добавлении '{category_name}': {str(e)}")
        
        print(f"\n{'='*60}")
        print(f"Готово! Успешно добавлено категорий: {added_count}/{len(CATEGORIES)}")
        print(f"{'='*60}")
        
        # Показываем все добавленные категории
        print("\nПолный список категорий в системе:")
        categories = service.get_categories()
        for cat in categories:
            print(f"  • ID {cat['category_id']}: {cat['category_name']}")
            
    except Exception as e:
        print(f"Ошибка подключения к БД: {str(e)}")
        print("Убедитесь, что MySQL запущен и БД создана.")

if __name__ == "__main__":
    populate_categories()
