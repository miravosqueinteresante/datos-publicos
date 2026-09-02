import unittest
from connectors.ande.validators import validate_yacyreta

def _r(ind, val, fi="2020-01-01", ff="2020-12-31"):
    return {"indicador": ind, "valor": val, "fecha_inicio": fi, "fecha_fin": ff}

class TestYacyreta(unittest.TestCase):
    def test_ok(self):
        recs=[_r("suministro_argentina",13192.97),_r("suministro_paraguay",1664.31),_r("generacion_total",14857.29)]
        self.assertEqual(validate_yacyreta(recs),[])
    def test_fail(self):
        recs=[_r("suministro_argentina",10000),_r("suministro_paraguay",1664.31),_r("generacion_total",14857.29)]
        self.assertTrue(validate_yacyreta(recs))

if __name__=="__main__":
    unittest.main()
