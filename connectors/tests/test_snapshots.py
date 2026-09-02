import json, os, unittest, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
def _load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))

class TestSnapshots(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(_load("www/datos/ande-indicadores.json")),75)
        self.assertEqual(len(_load("www/datos/itaipu-indicadores.json")),135)
        self.assertEqual(len(_load("www/datos/yacyreta-indicadores.json")),7)
    def test_key_values(self):
        ande=_load("www/datos/ande-indicadores.json")
        v=next(r["valor"] for r in ande if r["indicador"]=="perdidas_distribucion")
        self.assertAlmostEqual(v,20.03,places=2)
        ita=_load("www/datos/itaipu-indicadores.json")
        v=next(r["valor"] for r in ita if r["indicador"]=="generacion_total" and r["fecha_inicio"]=="2025-01-01")
        self.assertAlmostEqual(v,72403,delta=72403*0.005)
        yac=_load("www/datos/yacyreta-indicadores.json")
        v=next(r["valor"] for r in yac if r["indicador"]=="generacion_total" and r["fecha_inicio"]=="2020-01-01")
        self.assertAlmostEqual(v,14857,delta=14857*0.005)

if __name__=="__main__":
    unittest.main()
