from typing import Protocol


class AvailabilityPolicy(Protocol):
    """Интерфейс для проверки доступности бронирования"""
    def check_availability(self, room: str, equipment: str) -> bool:
        ...


class Reservation:
    """Сущность заявки на бронирование"""
    def __init__(self, res_id: int, student_name: str, room: str, equipment: str) -> None:
        if isinstance(res_id, bool) or not isinstance(res_id, int) or res_id <= 0:
            raise ValueError("ID брони должен быть положительным числом")
        if not student_name or not student_name.strip():
            raise ValueError("Имя студента не может быть пустым")

        self.res_id = res_id
        self.student_name = student_name.strip()
        self.room = room
        self.equipment = equipment


class LaboratoryCalendar:
    """Класс календаря бронирований (Композиция)"""
    def __init__(self, policy: AvailabilityPolicy) -> None:
        self._reservations: dict[int, Reservation] = {}
        self.policy = policy  # Зависимость передается через конструктор

    def add_reservation(self, reservation: Reservation) -> bool:
        if reservation.res_id in self._reservations:
            raise ValueError(f"Бронь с ID {reservation.res_id} уже существует")
        
        # Проверка через переданную политику
        if self.policy.check_availability(reservation.room, reservation.equipment):
            self._reservations[reservation.res_id] = reservation
            return True
        return False

    def get_reservation(self, res_id: int) -> Reservation:
        if res_id not in self._reservations:
            raise KeyError(f"Бронь {res_id} не найдена")
        return self._reservations[res_id]

    def get_all(self) -> list[Reservation]:
        return list(self._reservations.values())
