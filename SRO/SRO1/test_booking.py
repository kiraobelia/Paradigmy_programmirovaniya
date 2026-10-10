"""
Модуль автоматических тестов (12 сценариев)
"""
import unittest
from models import Room, Booking
from logic import (
    calculate_board_price, get_days_difference, is_dates_overlap,
    make_discount_calculator, filter_rooms_fp, RoomFeaturePolicy,
    DateAvailabilityPolicy, CompositeBookingChecker, create_sample_rooms,
    make_booking, cancel_booking_by_id, get_hotel_occupancy_stats
)

class TestHotelBookingSystem(unittest.TestCase):

    def setUp(self):
        self.rooms = create_sample_rooms()
        self.bookings = []

    # 1. Нормальные сценарии
    def test_calculate_board_price_breakfast(self):
        res = calculate_board_price(10000, 'BREAKFAST', 2)
        self.assertEqual(res, 26000.0)

    def test_days_difference(self):
        days = get_days_difference('2026-10-01', '2026-10-05')
        self.assertEqual(days, 4)

    def test_make_booking_success(self):
        room = self.rooms[0]
        b = make_booking(10, "Тест Гость", room, '2026-10-10', '2026-10-12', 'NONE')
        self.assertEqual(b.status, "CONFIRMED")
        self.assertEqual(b.total_price, 30000.0)

    def test_discount_closure(self):
        discount_5 = make_discount_calculator(10.0)
        self.assertEqual(discount_5(100), 90.0)

    def test_cancel_booking(self):
        b = make_booking(1, "Гость", self.rooms[0], '2026-10-01', '2026-10-02', 'NONE')
        self.bookings.append(b)
        res = cancel_booking_by_id(self.bookings, 1)
        self.assertTrue(res)
        self.assertEqual(b.status, "CANCELLED")

    def test_occupancy_stats(self):
        stats = get_hotel_occupancy_stats(self.rooms, self.bookings)
        self.assertEqual(stats["occupied_rooms"], 0)

    # 2. Граничные сценарии
    def test_dates_overlap_exact_boundary(self):
        # Выезд первого совпадает с заездом второго (не должны пересекаться)
        overlap = is_dates_overlap('2026-10-01', '2026-10-05', '2026-10-05', '2026-10-10')
        self.assertFalse(overlap)

    def test_dates_overlap_inside(self):
        overlap = is_dates_overlap('2026-10-01', '2026-10-10', '2026-10-02', '2026-10-05')
        self.assertTrue(overlap)

    def test_zero_days_stay_fallback(self):
        days = get_days_difference('2026-10-01', '2026-10-01')
        self.assertEqual(days, 1)

    # 3. Ошибочные / Специфические сценарии
    def test_policy_no_match_view(self):
        policy = RoomFeaturePolicy()
        room = self.rooms[0]  # STREET
        self.assertFalse(policy.is_satisfied(room, {'view_type': 'LAKE'}))

    def test_cancel_non_existing_booking(self):
        res = cancel_booking_by_id(self.bookings, 999)
        self.assertFalse(res)

    def test_fp_filter_empty_result(self):
        res = filter_rooms_fp(self.rooms, category='NON_EXISTENT')
        self.assertEqual(len(res), 0)

if __name__ == '__main__':
    unittest.main()
