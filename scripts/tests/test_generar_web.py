import unittest, json, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generar_datos_web import fila_a_json, generar, categoria_es

CSV_EJEMPLO = """id,objeto,estado,categoria,tipo_procedimiento,comprador,valor_estimado,monto_adjudicado,monto_contratado,moneda,n_adjudicaciones,n_proveedores,proveedor,proveedores,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
ocds-a-1,Compra de insumos,complete,goods,open,Municipalidad de Asunción,150000000,150000000,,PYG,1,1,PEPE S.A.,PEPE S.A.,2026-01-01T00:00:00,2026-01-10T00:00:00,2026-01-20T00:00:00,https://x/1
ocds-a-2,Construcción,active,works,open,Municipalidad de Asunción,0,,,PYG,0,0,,,,2026-02-01T00:00:00,,,https://x/2
"""

class TestGenerarWeb(unittest.TestCase):
    def test_categoria_mapeada_a_espanol(self):
        for crudo, esperado in [("goods", "Bienes"), ("services", "Servicios"), ("works", "Obras"), ("", ""), ("otra", "otra")]:
            self.assertEqual(categoria_es(crudo), esperado)

    def test_fila_a_json_montos_numericos(self):
        fila = {"id": "ocds-1", "objeto": "X", "valor_estimado": "150000000",
                "monto_adjudicado": "150000000", "fecha_publicacion": "2026-01-01T00:00:00"}
        out = fila_a_json(fila)
        self.assertEqual(out["monto_adjudicado"], 150000000)
        self.assertEqual(out["monto"], 150000000)
        self.assertEqual(out["monto_nulo"], False)
    def test_fila_a_json_monto_vacio(self):
        out = fila_a_json({"id": "ocds-2", "objeto": "Y", "valor_estimado": "",
                           "monto_adjudicado": "", "fecha_publicacion": ""})
        self.assertEqual(out["monto"], 0)
        self.assertEqual(out["monto_nulo"], True)
    def test_generar_lee_diccionarios(self):
        filas = generar(CSV_EJEMPLO)
        self.assertEqual(len(filas), 2)
        self.assertEqual(filas[0]["proveedor"], "PEPE S.A.")

if __name__ == "__main__":
    unittest.main()