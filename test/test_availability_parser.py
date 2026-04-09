import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from suburbot.availability_parser import find_available_rooms_from_matrix


SHEET_VALUES = [
    ["habitacion", "2026-04-10", "2026-04-11", "2026-04-12"],
    ["H1", "disponible", "ocupado", "disponible"],
    ["H2", "disponible", "disponible", "disponible"],
    ["H3", "ocupado", "disponible", "disponible"],
]


class AvailabilityParserTest(unittest.TestCase):
    def test_finds_rooms_available_for_every_night_in_the_stay(self):
        result = find_available_rooms_from_matrix(SHEET_VALUES, "2026-04-10", "2026-04-12")

        self.assertEqual(
            result,
            {
                "check_in": "2026-04-10",
                "check_out": "2026-04-12",
                "nights": ["2026-04-10", "2026-04-11"],
                "available_rooms": ["H2"],
            },
        )

    def test_treats_checkout_as_exclusive(self):
        result = find_available_rooms_from_matrix(SHEET_VALUES, "2026-04-11", "2026-04-12")

        self.assertEqual(result["available_rooms"], ["H2", "H3"])

    def test_rejects_invalid_date_ranges(self):
        with self.assertRaisesRegex(ValueError, "check_out must be after check_in"):
            find_available_rooms_from_matrix(SHEET_VALUES, "2026-04-12", "2026-04-12")

    def test_fails_when_a_requested_date_is_missing_from_the_sheet_header(self):
        with self.assertRaisesRegex(ValueError, "Date 2026-04-13 was not found"):
            find_available_rooms_from_matrix(SHEET_VALUES, "2026-04-13", "2026-04-14")


if __name__ == "__main__":
    unittest.main()
