def interactive_booking(rooms, bookings):
    print("\n--- Новое бронирование (вводите данные сами) ---")
    guest = input("ФИО гостя: ")
    category = input("Категория (LUX / FAMILY / STANDARD, Enter - любая): ").strip().upper()
    view = input("Вид (LAKE / STREET / YARD / SIDE, Enter - любой): ").strip().upper()
    building = input("Корпус (MAIN / SIDE_WING, Enter - любой): ").strip().upper()
    check_in = input("Дата заезда (например 2026-11-10): ").strip()
    check_out = input("Дата выезда (например 2026-11-12): ").strip()
    board = input("Питание (NONE / BREAKFAST / FULL_BOARD): ").strip().upper()

    criteria = {'check_in': check_in, 'check_out': check_out}
    if category:
        criteria['category'] = category
    if view:
        criteria['view_type'] = view
    if building:
        criteria['building'] = building

    available = filter_available_rooms(rooms, bookings, criteria)
    if available:
        b = make_booking(len(bookings) + 1, guest, available[0], check_in, check_out, board)
        bookings.append(b)
        print(f"Успешно создано: {b}")
    else:
        print("Свободных номеров по таким условиям нет.")
