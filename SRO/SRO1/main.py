"""
Точка входа (Лекции 1, 2, 4)
"""
from models import Room, Booking
from logic import (
    create_sample_rooms, filter_available_rooms, make_booking,
    cancel_booking_by_id, get_hotel_occupancy_stats, format_booking_report,
    filter_rooms_fp, calculate_total_revenue
)

def demonstrate_paradigm_comparison(rooms):
    """
    Лекция 1: Сравнение способов отбора номеров (Императивный vs Функциональный)
    """
    print("\n--- ЛЕКЦИЯ 1: Сравнение парадигм программирования ---")
    
    # 1. Императивный подход
    imp_result = []
    for r in rooms:
        if r.category == 'LUX' and r.view_type == 'LAKE':
            imp_result.append(r)
    print(f"Императивный подход (нашел): {len(imp_result)} шт.")

    # 2. Функциональный подход (filter + lambda)
    fp_result = list(filter(lambda r: r.category == 'LUX' and r.view_type == 'LAKE', rooms))
    print(f"Функциональный подход (нашел): {len(fp_result)} шт.")


def run_imperative_prototype():
    """
    Лекция 2: Рабочий императивный прототип (переменные, условия, циклы)
    """
    print("\n--- ЛЕКЦИЯ 2: Императивный прототип бронирования ---")
    rooms_data = [
        {"id": 1, "cat": "LUX", "price": 40000, "free": True},
        {"id": 2, "cat": "STANDARD", "price": 15000, "free": True}
    ]
    
    req_cat = "LUX"
    found_id = -1
    
    i = 0
    while i < len(rooms_data):
        if rooms_data[i]["cat"] == req_cat and rooms_data[i]["free"]:
            found_id = rooms_data[i]["id"]
            rooms_data[i]["free"] = False
            break
        i += 1
        
    if found_id != -1:
        print(f"[Успех] Номер #{found_id} забронирован через императивный прототип.")
    else:
        print("[Отказ] Нет свободных номеров.")


def main():
    print("==================================================")
    print("   СИСТЕМА БРОНИРОВАНИЯ ОТЕЛЯ (Мини-проект по СРО)")
    print("==================================================")

    # 1. Инициализация данных
    rooms = create_sample_rooms()
    bookings = []
    
    # Демонстрация лекций 1 и 2
    demonstrate_paradigm_comparison(rooms)
    run_imperative_prototype()

    # 2. Выполнение основного сценария бронирования (ООП + Политики)
    print("\n--- Основной сценарий работы системы ---")
    
    # Заявка 1: Гость хочет Люкс с видом на озеро в Центральном корпусе
    criteria_1 = {
        'category': 'LUX',
        'view_type': 'LAKE',
        'building': 'MAIN',
        'check_in': '2026-11-01',
        'check_out': '2026-11-05'
    }
    
    available_1 = filter_available_rooms(rooms, bookings, criteria_1)
    if available_1:
        b1 = make_booking(1, "Кирилл Бледный", available_1[0], '2026-11-01', '2026-11-05', 'FULL_BOARD', discount_rate=5.0)
        bookings.append(b1)
        print(f"Успешно создано: {b1}")
    
    # Заявка 2: Семейный номер, вид во двор, раздельные кровати
    criteria_2 = {
        'category': 'FAMILY',
        'view_type': 'YARD',
        'bed_type': 'TWIN',
        'check_in': '2026-11-01',
        'check_out': '2026-11-03'
    }
    
    available_2 = filter_available_rooms(rooms, bookings, criteria_2)
    if available_2:
        b2 = make_booking(2, "Кайрат Нуртас", available_2[0], '2026-11-01', '2026-11-03', 'BREAKFAST')
        bookings.append(b2)
        print(f"Успешно создано: {b2}")

    # 3. Печать отчета и статистики
    print("\n" + format_booking_report(bookings))
    
    stats = get_hotel_occupancy_stats(rooms, bookings)
    print(f"\nСтатистика загрузки отеля: {stats}")
    
    # Выручка через Лекцию 8 (FP pipeline)
    revenue = calculate_total_revenue(bookings)
    print(f"Общая подтвержденная выручка: {revenue} тг")

if __name__ == "__main__":
    main()
