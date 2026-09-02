import unittest
from .. import validators


class TestRelativeChange(unittest.TestCase):
    def test_growth(self):
        self.assertAlmostEqual(validators.relative_change(26154, 29419), 29419 / 26154)

    def test_zero_prev(self):
        self.assertIsNone(validators.relative_change(0, 100))


class TestIsAnomaly(unittest.TestCase):
    def test_extreme_jump(self):
        self.assertTrue(validators.is_anomaly(29419, 294190))

    def test_normal_growth(self):
        self.assertFalse(validators.is_anomaly(26154, 29419))  # +12,5%

    def test_drop_to_zero(self):
        self.assertTrue(validators.is_anomaly(29419, 0))


class TestIsDuplicate(unittest.TestCase):
    def test_duplicate(self):
        rec = {"indicador": "consumo_total", "fecha_inicio": "2025-01-01",
               "fecha_fin": "2025-12-31", "valor": 29.419}
        self.assertTrue(validators.is_duplicate(rec, [rec]))

    def test_not_duplicate(self):
        a = {"indicador": "consumo_total", "fecha_inicio": "2025-01-01",
             "fecha_fin": "2025-12-31", "valor": 29.419}
        b = {"indicador": "demanda_maxima", "fecha_inicio": "2025-01-01",
             "fecha_fin": "2025-12-31", "valor": 5280}
        self.assertFalse(validators.is_duplicate(a, [b]))


class TestPeriodsOverlap(unittest.TestCase):
    def test_overlap(self):
        a = {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
        b = {"fecha_inicio": "2025-06-01", "fecha_fin": "2026-06-30"}
        self.assertTrue(validators.periods_overlap(a, b))

    def test_no_overlap(self):
        a = {"fecha_inicio": "2024-01-01", "fecha_fin": "2024-12-31"}
        b = {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
        self.assertFalse(validators.periods_overlap(a, b))


def _rec(indicador, valor, fi="2025-01-01", ff="2025-12-31"):
    return {"indicador": indicador, "valor": valor, "fecha_inicio": fi, "fecha_fin": ff}


class TestValidateInvariants(unittest.TestCase):
    def test_ok(self):
        recs = [
            _rec("perdidas_distribucion", 20.03, "2025-12-01", "2025-12-31"),
            _rec("perdidas_transmision", 1.86, "2025-12-01", "2025-12-31"),
            _rec("perdidas_totales", 21.89, "2025-12-01", "2025-12-31"),
            _rec("consumo_categoria_residencial", 600),
            _rec("consumo_categoria_industrial", 400),
            _rec("consumo_total", 1000),
            _rec("clientes_categoria_residencial", 800),
            _rec("clientes_categoria_industrial", 200),
            _rec("clientes_total", 1000),
        ]
        self.assertEqual(validators.validate_invariants(recs), [])

    def test_perdidas_fail_21_89(self):
        recs = [
            _rec("perdidas_distribucion", 21.89, "2025-12-01", "2025-12-31"),
            _rec("perdidas_transmision", 1.86, "2025-12-01", "2025-12-31"),
            _rec("perdidas_totales", 21.89, "2025-12-01", "2025-12-31"),
        ]
        errs = validators.validate_invariants(recs)
        self.assertTrue(any("perdidas" in e.lower() for e in errs))

    def test_consumo_fail(self):
        recs = [
            _rec("consumo_categoria_residencial", 600),
            _rec("consumo_categoria_industrial", 400),
            _rec("consumo_total", 1500),
        ]
        self.assertTrue(len(validators.validate_invariants(recs)) > 0)

    def test_clientes_fail(self):
        recs = [
            _rec("clientes_categoria_residencial", 800),
            _rec("clientes_categoria_industrial", 200),
            _rec("clientes_total", 1010),
        ]
        self.assertTrue(len(validators.validate_invariants(recs)) > 0)


if __name__ == "__main__":
    unittest.main()
