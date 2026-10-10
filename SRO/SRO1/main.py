class Room:
    """Класс, описывающий номер в отеле."""
    def __init__(self, room_id: int, category: str, building: str, view_type: str, bed_type: str, base_price: float):
        self.room_id = room_id
        self.category = category        # 'LUX', 'FAMILY', 'STANDARD'
        self.building = building        # 'MAIN', 'SIDE_WING'
        self.view_type = view_type      # 'STREET', 'YARD', 'LAKE', 'SIDE'
        self.bed_type = bed_type        # 'TWIN', 'DOUBLE'
        self.base_price = base_price

    def __repr__(self):
        return f"Комната #{self.room_id} [{self.category}] | Корпус: {self.building} | Вид: {self.view_type} | Кровати: {self.bed_type} | {self.base_price} тг/ночь"


class Booking:
    """Класс бронирования с защищенными полями (инкапсуляция)."""
    def __init__(self, booking_id: int, guest_name: str, room: Room, check_in: str, check_out: str, board_type: str, total_price: float):
        self.booking_id = booking_id
        self.guest_name = guest_name
        self.room = room
        # Приватные свойства для защиты состояния
        self._check_in = check_in
        self._check_out = check_out
        self.board_type = board_type    # 'BREAKFAST', 'FULL_BOARD', 'NONE'
        self.total_price = total_price
        self.status = "CONFIRMED"       # 'CONFIRMED' или 'CANCELLED'

    @property
    def check_in(self):
        return self._check_in

    @property
    def check_out(self):
        return self._check_out

    def cancel(self):
        self.status = "CANCELLED"

    def __repr__(self):
        return f"Бронь #{self.booking_id} ({self.guest_name}) | Комната #{self.room.room_id} | {self.check_in} - {self.check_out} | Питание: {self.board_type} | Сумма: {self.total_price} тг [{self.status}]"
