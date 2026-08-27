import unittest, json, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generar_datos_web import fila_a_json, generar, categoria_es
from generar_datos_web import presupuesto_filas_a_json

CSV_EJEMPLO = """id,objeto,estado,categoria,tipo_procedimiento,comprador,proveedor,monto,moneda,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
ocds-a-1,Compra de insumos,complete,goods,open,Municipalidad de Asunción,PEPE S.A.,150000000,PYG,2026-01-01T00:00:00,2026-01-10T00:00:00,2026-01-20T00:00:00,https://x/1
ocds-a-2,Construcción,active,works,open,Municipalidad de Asunción,,0,PYG,2026-02-01T00:00:00,,,,https://x/2
"""

class TestGenerarWeb(unittest.TestCase):
    def test_categoria_mapeada_a_espanol(self):
        for crudo, esperado in [("goods", "Bienes"), ("services", "Servicios"), ("works", "Obras"), ("", ""), ("otra", "otra")]:
            self.assertEqual(categoria_es(crudo), esperado)

    def test_fila_a_json_montos_numericos(self):
        fila = {"id": "ocds-1", "objeto": "X", "monto": "150000000", "fecha_publicacion": "2026-01-01T00:00:00"}
        out = fila_a_json(fila)
        self.assertEqual(out["monto"], 150000000)
        self.assertEqual(out["monto_nulo"], False)
    def test_fila_a_json_monto_vacio(self):
        out = fila_a_json({"id": "ocds-2", "objeto": "Y", "monto": "", "fecha_publicacion": ""})
        self.assertEqual(out["monto"], 0)
        self.assertEqual(out["monto_nulo"], True)
    def test_generar_lee_diccionarios(self):
        filas = generar(CSV_EJEMPLO)
        self.assertEqual(len(filas), 2)
        self.assertEqual(filas[0]["proveedor"], "PEPE S.A.")

class TestPresupuestoJson(unittest.TestCase):
    def test_presupuesto_filas_a_json(self):
        filas_csv = [
            ["2024", "100", "Servicios Personales", "788089.0", "727234.0", "92.28", "Rendición de Cuentas 2024", "url"],
            ["2024", "TOTAL", "TOTAL GENERAL", "2360168.0", "1165830.0", "49.4", "Rendición de Cuentas 2024", "url"],
        ]
        out = presupuesto_filas_a_json(filas_csv)
        self.assertEqual(out[0]["nivel"], "100")
        self.assertEqual(out[0]["presupuesto_vigente"], 788089.0)
        self.assertEqual(out[0]["porcentaje_ejecucion"], 92.28)
        self.assertEqual(out[1]["nivel"], "TOTAL")
    def test_presupuesto_vacio(self):
        self.assertEqual(presupuesto_filas_a_json([]), [])

if __name__ == "__main__":
    unittest.main()