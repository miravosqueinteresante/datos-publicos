import unittest, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from presupuesto_2024 import parsear_fila, validar_totales, normalizar_numero

class TestParsear(unittest.TestCase):
    def test_normalizar_numero(self):
        # punto = separador de miles (valores en millones de guaraníes del PDF)
        self.assertEqual(normalizar_numero("788.089"), 788089.0)
        self.assertEqual(normalizar_numero("1.253.270"), 1253270.0)
        self.assertEqual(normalizar_numero("53%"), None)
    def test_parsear_fila_validar_campos(self):
        f = parsear_fila(["100", "Servicios Personales", "788.089", "727.234", "92%"])
        self.assertEqual(f["nivel"], "100")
        self.assertEqual(f["denominacion"], "Servicios Personales")
        self.assertEqual(f["presupuesto_vigente"], 788089.0)
        self.assertEqual(f["obligado"], 727234.0)
        self.assertEqual(round(f["porcentaje_ejecucion"], 2), 92.28)
    def test_validar_totales_ok(self):
        filas = [
            {"nivel": "100", "presupuesto_vigente": 788089.0, "obligado": 727234.0},
            {"nivel": "200", "presupuesto_vigente": 232517.0, "obligado": 114346.0},
        ]
        errores = validar_totales(filas, total_vigente=1020606.0, total_obligado=841580.0)
        self.assertEqual(len(errores), 0)
    def test_validar_totales_roto(self):
        filas = [{"nivel": "100", "presupuesto_vigente": 1.0, "obligado": 1.0}]
        errores = validar_totales(filas, total_vigente=999.0, total_obligado=1.0)
        self.assertGreater(len(errores), 0)

if __name__ == "__main__":
    unittest.main()