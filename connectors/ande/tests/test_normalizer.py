import unittest
from .. import normalizer


class TestParseNumber(unittest.TestCase):
    def test_thousands_dot(self):
        self.assertEqual(normalizer.parse_number("29.419"), 29419.0)

    def test_decimal_comma(self):
        self.assertEqual(normalizer.parse_number("24,40"), 24.4)

    def test_percent_strips_symbol(self):
        self.assertEqual(normalizer.parse_number("87,6 %"), 87.6)

    def test_power_mw(self):
        self.assertEqual(normalizer.parse_number("5.280"), 5280.0)


class TestParsePeriod(unittest.TestCase):
    def test_year(self):
        self.assertEqual(
            normalizer.parse_period("2025"),
            ("2025-01-01", "2025-12-31"),
        )

    def test_month_abbrev(self):
        self.assertEqual(
            normalizer.parse_period("dic-2025"),
            ("2025-12-01", "2025-12-31"),
        )


class TestConvertEnergy(unittest.TestCase):
    def test_mwh_to_gwh(self):
        self.assertEqual(normalizer.convert_energy(1000, "MWh"), (1.0, "GWh"))

    def test_kwh_to_gwh(self):
        self.assertEqual(normalizer.convert_energy(1_000_000, "kWh"), (1.0, "GWh"))

    def test_gwh_passthrough(self):
        self.assertEqual(normalizer.convert_energy(29.419, "GWh"), (29.419, "GWh"))


if __name__ == "__main__":
    unittest.main()
