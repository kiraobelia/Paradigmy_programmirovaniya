
from functools import reduce
from datetime import datetime
from models import Room, Booking


def calculate_board_price(base_price: float, board_type: str, days: int) -> float:
    """Чистая функция: рассчитывает стоимость проживания с учетом питания."""
    markup = 0.0
    if board_type == 'BREAKFAST':
        markup = 3000.0
    elif board_type == 'FULL_BOARD':
        markup = 8000.0
    
    return (base_price + markup) * days


def get_days_difference(date_start_str: str, date_end_str: str) -> int:
    """Чистая функция: вычисляет кол-во дней между датами (формат YYYY-MM-DD)."""
    d1 = datetime.strptime(date_start_str, "%Y-%m-%d")
    d2 = datetime.strptime(date_end_str, "%Y-%m-%d")
    delta = (d2 - d1).days
    return delta if delta > 0 else 1


def is_dates_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    """Чистая функция: проверяет пересечение двух интервалов дат."""
    d1_start = datetime.strptime(start1, "%Y-%m-%d")
    d1_end = datetime.strptime(end1, "%Y-%m-%d")
    d2_start = datetime.strptime(start2, "%Y-%m-%d")
    d2_end = datetime.strptime(end2, "%Y-%m-%d")
    return max(d1_start, d2_start) < min(d1_end, d2_end)


def find_next_available_day_recursive(start_date_str: str, occupied_dates: list, step: int = 0) -> str:
    """Лекция 7: Рекурсивный поиск ближайшей свободной даты заселения."""
    current_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    # Добавляем дни рекурсивно
    check_date = current_date.replace(day=current_date.day + step)
    check_str = check_date.strftime("%Y-%m-%d")
    
    if check_str not in occupied_dates or step > 30:
        return check_str
    
    return find_next_available_day_recursive(start_date_str, occupied_dates, step + 1)


class BaseAvailabilityPolicy:
    """Базовый класс политики доступности."""
    def is_satisfied(self, room: Room, criteria: dict) -> bool:
        raise NotImplementedError("Метод должен быть переопределен")


class RoomFeaturePolicy(BaseAvailabilityPolicy):
    """Политика проверки параметров комнаты (корпус, вид, тип кровати, категория)."""
    def is_satisfied(self, room: Room, criteria: dict) -> bool:
        if 'building' in criteria and room.building != criteria['building']:
            return False
        if 'view_type' in criteria and room.view_type != criteria['view_type']:
            return False
        if 'bed_type' in criteria and room.bed_type != criteria['bed_type']:
            return False
        if 'category' in criteria and room.category != criteria['category']:
            return False
        return True


class DateAvailabilityPolicy(BaseAvailabilityPolicy):
    """Политика проверки занятости комнаты на указанные даты."""
    def __init__(self, existing_bookings: list):
        self.existing_bookings = existing_bookings

    def is_satisfied(self, room: Room, criteria: dict) -> bool:
        req_start = criteria.get('check_in')
        req_end = criteria.get('check_out')
        if not req_start or not req_end:
            return True

        for b in self.existing_bookings:
            if b.status == "CONFIRMED" and b.room.room_id == room.room_id:
                if is_dates_overlap(req_start, req_end, b.check_in, b.check_out):
                    return False
        return True


class CompositeBookingChecker:
    """Композитор политик проверки."""
    def __init__(self, policies: list):
        self.policies = policies

    def check_room(self, room: Room, criteria: dict) -> bool:
        return all(policy.is_satisfied(room, criteria) for policy in self.policies)


def make_discount_calculator(discount_percent: float):
    """Замыкание (Closure): создает функцию для расчета стоимости со скидкой."""
    def apply_discount(amount: float) -> float:
        return amount * (1.0 - discount_percent / 100.0)
    return apply_discount


def filter_rooms_fp(rooms: list, category=None, view_type=None, building=None) -> list:
    """Обработка через filter (Функциональная парадигма)."""
    filtered = rooms
    if category:
        filtered = list(filter(lambda r: r.category == category, filtered))
    if view_type:
        filtered = list(filter(lambda r: r.view_type == view_type, filtered))
    if building:
        filtered = list(filter(lambda r: r.building == building, filtered))
    return filtered


def calculate_total_revenue(bookings: list) -> float:
    """Расчет общей выручки через reduce и map."""
    confirmed_bookings = filter(lambda b: b.status == "CONFIRMED", bookings)
    prices = map(lambda b: b.total_price, confirmed_bookings)
    return reduce(lambda x, y: x + y, prices, 0.0)


def create_sample_rooms() -> list:
    """1. Создание исходных данных."""
    return [
        Room(101, 'STANDARD', 'MAIN', 'STREET', 'TWIN', 15000),
        Room(102, 'STANDARD', 'MAIN', 'YARD', 'DOUBLE', 16000),
        Room(201, 'LUX', 'MAIN', 'LAKE', 'DOUBLE', 40000),
        Room(202, 'LUX', 'SIDE_WING', 'SIDE', 'TWIN', 35000),
        Room(301, 'FAMILY', 'MAIN', 'LAKE', 'DOUBLE', 30000),
        Room(302, 'FAMILY', 'SIDE_WING', 'YARD', 'TWIN', 25000),
    ]

def filter_available_rooms(rooms: list, existing_bookings: list, criteria: dict) -> list:
    """2. Подбор номеров по композиции политик."""
    feature_policy = RoomFeaturePolicy()
    date_policy = DateAvailabilityPolicy(existing_bookings)
    checker = CompositeBookingChecker([feature_policy, date_policy])
    
    return [room for room in rooms if checker.check_room(room, criteria)]

def make_booking(booking_id: int, guest_name: str, room: Room, check_in: str, check_out: str, board_type: str, discount_rate: float = 0.0) -> Booking:
    """3. Функция создания бронирования с дисконтом."""
    days = get_days_difference(check_in, check_out)
    base_cost = calculate_board_price(room.base_price, board_type, days)
    
    discount_calc = make_discount_calculator(discount_rate)
    final_cost = discount_calc(base_cost)
    
    return Booking(booking_id, guest_name, room, check_in, check_out, board_type, final_cost)

def cancel_booking_by_id(bookings: list, booking_id: int) -> bool:
    """4. Отмена брони по ID."""
    for b in bookings:
        if b.booking_id == booking_id:
            b.cancel()
            return True
    return False

def get_hotel_occupancy_stats(rooms: list, bookings: list) -> dict:
    """5. Расчет статистики загрузки отеля."""
    active_bookings = [b for b in bookings if b.status == "CONFIRMED"]
    occupied_room_ids = {b.room.room_id for b in active_bookings}
    
    total_rooms = len(rooms)
    occupied_count = len(occupied_room_ids)
    occupancy_rate = (occupied_count / total_rooms * 100) if total_rooms > 0 else 0.0
    
    return {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_count,
        "free_rooms": total_rooms - occupied_count,
        "occupancy_rate": round(occupancy_rate, 2)
    }

def format_booking_report(bookings: list) -> str:
    """6. Генерация отчета по бронированиям."""
    lines = ["=== РЕЕСТР БРОНИРОВАНИЙ ==="]
    for b in bookings:
        lines.append(str(b))
    return "\n".join(lines)
