from functools import reduce
from models import AvailabilityPolicy, Reservation


# 1. Взаимозаменяемые политики (Полиморфизм)
class RoomPolicy:
    """Простая политика: доступно всё, кроме закрытых комнат"""
    def check_availability(self, room: str, equipment: str) -> bool:
        blocked_rooms = ["Кабинет-101", "Лаб-303"]
        return room not in blocked_rooms


class EquipmentPolicy:
    """Строгая политика: проверяет наличие оборудования"""
    def check_availability(self, room: str, equipment: str) -> bool:
        unavailable_equipment = ["Осциллограф", "3D-принтер"]
        return equipment not in unavailable_equipment


# 2. Чистые функции
def is_valid_room_name(room: str) -> bool:
    """Чистая функция проверки названия комнаты"""
    return len(room) > 0 and room.startswith("Лаб")


def format_reservation(res: Reservation) -> str:
    """Чистая функция форматирования брони"""
    return f"Бронь #{res.res_id} | {res.student_name} | Помещение: {res.room} | Оборудование: {res.equipment}"


# 3. Рекурсивная функция
def count_reservations_recursive(reservations: list[Reservation]) -> int:
    """Рекурсивный подсчет количества броней"""
    if not reservations:
        return 0
    return 1 + count_reservations_recursive(reservations[1:])


# 4. Конвейер с map, filter, reduce
def process_reservations_pipeline(reservations: list[Reservation], policy: AvailabilityPolicy):
    """Конвейер обработки с помощью FP"""
    # Фильтруем доступные брони
    approved = list(filter(lambda r: policy.check_availability(r.room, r.equipment), reservations))
    
    # Формируем текстовые строки через map
    approved_texts = list(map(format_reservation, approved))
    
    # Считаем общее число одобренных через reduce
    total_approved = reduce(lambda acc, _: acc + 1, approved, 0)

    return approved, approved_texts, total_approved
