import unittest
from connectors.ande.validators import validate_itaipu

def _r(ind, val, fi="2025-01-01", ff="2025-12-31"):
    return {"indicador": ind, "valor": val, "fecha_inicio": fi, "fecha_fin": ff}

class TestItaipu(unittest.TestCase):
    def test_ok(self):
        recs=[_r("generacion_sector_50hz",38789.26),_r("generacion_sector_60hz",33613.76),_r("generacion_total",72403.02),_r("suministro_paraguay",25761.41),_r("suministro_brasil",46641.60)]
        self.assertEqual(validate_itaipu(recs),[])
    def test_sector_fail(self):
        recs=[_r("generacion_sector_50hz",30000),_r("generacion_sector_60hz",33613.76),_r("generacion_total",72403.02),_r("suministro_paraguay",25761.41),_r("suministro_brasil",46641.60)]
        self.assertTrue(validate_itaipu(recs))
    def test_suministro_fail(self):
        recs=[_r("generacion_sector_50hz",38789.26),_r("generacion_sector_60hz",33613.76),_r("generacion_total",72403.02),_r("suministro_paraguay",20000),_r("suministro_brasil",46641.60)]
        self.assertTrue(validate_itaipu(recs))

if __name__=="__main__":
    unittest.main()
