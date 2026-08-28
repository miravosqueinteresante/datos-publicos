import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dncp_contrataciones import es_de_asuncion
from dncp_contrataciones import es_entidad_por_sicp
from dncp_contrataciones import verificar_consistencia
from dncp_contrataciones import anio_sicp_desde_args
from dncp_contrataciones import mapear_fila
from dncp_contrataciones import validar
from dncp_contrataciones import parse_csv_robusto
from dncp_contrataciones import indexar_awards
from dncp_contrataciones import indexar_suppliers
from dncp_contrataciones import indexar_contracts

class TestEsEntidadPorSicp(unittest.TestCase):
    def test_filtra_por_sicp_108(self):
        fila = {"compiledRelease/buyer/id": "DNCP-SICP-CODE-108"}
        self.assertTrue(es_entidad_por_sicp(fila, "108"))
    def test_rechaza_otro_sicp(self):
        fila = {"compiledRelease/buyer/id": "DNCP-SICP-CODE-226"}
        self.assertFalse(es_entidad_por_sicp(fila, "108"))
    def test_rechaza_sin_id(self):
        self.assertFalse(es_entidad_por_sicp({}, "108"))

class TestFiltrar(unittest.TestCase):
    def test_nombre_municipalidad(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asuncion"))
    def test_nombre_con_tilde(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asunción"))
    def test_no_es_otro_org(self):
        self.assertFalse(es_de_asuncion("Ministerio de Salud Pública"))
    def test_no_universidad(self):
        self.assertFalse(es_de_asuncion("Universidad Nacional de Asunción"))

class TestMapear(unittest.TestCase):
    def test_extrae_campos_clave(self):
        fila = {
            "compiledRelease/id": "ocds-03ad3f-999",
            "compiledRelease/tender/title": "Construcción de vereda",
            "compiledRelease/tender/status": "active",
            "compiledRelease/buyer/name": "Municipalidad de Asuncion",
            "compiledRelease/tender/value/amount": "150000000",
            "compiledRelease/tender/value/currency": "PYG",
        }
        salida = mapear_fila(fila, {}, {}, {})
        self.assertEqual(salida["id"], "ocds-03ad3f-999")
        self.assertEqual(salida["objeto"], "Construcción de vereda")
        self.assertEqual(salida["valor_estimado"], "150000000")
        self.assertEqual(salida["monto_adjudicado"], "")

    def test_separa_valor_y_adjudicado(self):
        fila = {
            "compiledRelease/id": "ocds-x",
            "compiledRelease/tender/value/amount": "1000",
            "compiledRelease/tender/value/currency": "PYG",
        }
        awards = {"ocds-x": [{"monto": "400", "fecha": "2026-01-01", "estado": "active"}]}
        suppliers = {"ocds-x": {0: ["Empresa A"]}}
        contracts = {"ocds-x": [{"monto": "380", "fecha": "2026-02-01"}]}
        s = mapear_fila(fila, awards, suppliers, contracts)
        self.assertEqual(s["valor_estimado"], "1000")
        self.assertEqual(s["monto_adjudicado"], "400")
        self.assertEqual(s["monto_contratado"], "380")
        self.assertEqual(s["n_adjudicaciones"], 1)
        self.assertEqual(s["n_proveedores"], 1)
        self.assertEqual(s["proveedor"], "Empresa A")

    def test_sin_adjudicacion_deja_adjudicado_vacio(self):
        fila = {"compiledRelease/id": "ocds-y",
                "compiledRelease/tender/value/amount": "500",
                "compiledRelease/tender/value/currency": "PYG"}
        s = mapear_fila(fila, {}, {}, {})
        self.assertEqual(s["monto_adjudicado"], "")
        self.assertEqual(s["n_adjudicaciones"], 0)

    def test_multiples_adjudicaciones_se_sum(self):
        fila = {"compiledRelease/id": "ocds-z",
                "compiledRelease/tender/value/amount": "10",
                "compiledRelease/tender/value/currency": "PYG"}
        awards = {"ocds-z": [{"monto": "100", "fecha": "2026-01-01", "estado": "active"},
                              {"monto": "50", "fecha": "2026-01-02", "estado": "active"}]}
        suppliers = {"ocds-z": {0: ["A"], 1: ["B"]}}
        s = mapear_fila(fila, awards, suppliers, {})
        self.assertEqual(s["monto_adjudicado"], "150")
        self.assertEqual(s["n_adjudicaciones"], 2)
        self.assertEqual(s["n_proveedores"], 2)
        self.assertEqual(s["proveedores"], "A | B")
    def test_campos_faltantes_quedan_vacios(self):
        salida = mapear_fila({"compiledRelease/id": "x"}, {}, {}, {})
        self.assertEqual(salida["objeto"], "")

    def test_url_usa_tender_id_uuid(self):
        fila = {
            "compiledRelease/id": "uuid-1-1769",
            "compiledRelease/tender/id": "uuid-1",
            "compiledRelease/tender/title": "Obra vial",
        }
        salida = mapear_fila(fila, {}, {}, {})
        self.assertEqual(
            salida["url_muni"],
            "https://www.contrataciones.gov.py/licitaciones/convocatoria/uuid-1.html",
        )

    def test_tipo_procedimiento_usa_etiqueta_espanol(self):
        fila = {
            "compiledRelease/id": "uuid-2",
            "compiledRelease/tender/procurementMethod": "direct",
            "compiledRelease/tender/procurementMethodDetails": "Menor cuantía nacional",
        }
        salida = mapear_fila(fila, {}, {}, {})
        self.assertEqual(salida["tipo_procedimiento"], "Menor cuantía nacional")

class TestValidar(unittest.TestCase):
    def test_filas_validas(self):
        filas = [
            {"id": "a", "objeto": "ob", "valor_estimado": "150"},
            {"id": "b", "objeto": "ob2", "valor_estimado": "300"},
        ]
        errores = validar(filas)
        self.assertEqual(len(errores), 0)
    def test_detecta_id_vacio(self):
        filas = [{"id": "", "objeto": "ob"}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
    def test_detecta_objeto_vacio(self):
        filas = [{"id": "a", "objeto": ""}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
    def test_detecta_valor_no_numerico(self):
        filas = [{"id": "a", "objeto": "ob", "valor_estimado": "ABC"}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)

class TestConsistencia(unittest.TestCase):
    def test_por_nombre_igual_que_por_id(self):
        filas = [
            {"compiledRelease/buyer/name": "Municipalidad de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-108"},
            {"compiledRelease/buyer/name": "Municipalidad de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-108"},
            {"compiledRelease/buyer/name": "Ministerio de Salud", "compiledRelease/buyer/id": "DNCP-SICP-CODE-80"},
        ]
        ok, msg = verificar_consistencia(filas)
        self.assertTrue(ok)
        self.assertIn("2", msg)
    def test_por_nombre_y_id_difieren(self):
        filas = [
            {"compiledRelease/buyer/name": "Municipalidad de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-108"},
            {"compiledRelease/buyer/name": "Municipalidad de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-108"},
            {"compiledRelease/buyer/name": "Municipalidad de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-999"},
        ]
        ok, msg = verificar_consistencia(filas)
        self.assertFalse(ok)
    def test_consistencia_otra_entidad(self):
        filas = [
            {"compiledRelease/buyer/name": "Universidad Nacional de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-226"},
            {"compiledRelease/buyer/name": "Universidad Nacional de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-226"},
            {"compiledRelease/buyer/name": "Ministerio de Salud", "compiledRelease/buyer/id": "DNCP-SICP-CODE-80"},
        ]
        ok, msg = verificar_consistencia(filas, sicp="226")
        self.assertTrue(ok)
        self.assertIn("2", msg)

class TestAnioArgs(unittest.TestCase):
    def test_sin_args_default_2026(self):
        self.assertEqual(anio_sicp_desde_args([]), ("2026", "108"))
    def test_con_arg(self):
        self.assertEqual(anio_sicp_desde_args(["dncp_contrataciones.py", "2024"]), ("2024", "108"))
    def test_arg_invalido_default(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "abc"]), ("2026", "108"))

class TestArgsSicp(unittest.TestCase):
    def test_default_sicp_108(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "2026"]), ("2026", "108"))
    def test_con_sicp(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "2024", "226"]), ("2024", "226"))
    def test_con_sicp_solo(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "2026", "999"]), ("2026", "999"))

class TestParseCsvRobusto(unittest.TestCase):
    def test_valor_con_coma_se_preserva(self):
        # header con comillas internas = 1 campo; el dato 3 pasa intacto
        texto = 'a,b,"texto,con coma",d\n1,2,3,4\n'
        filas = parse_csv_robusto(texto)
        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["a"], "1")
        self.assertEqual(filas[0]["d"], "4")
        self.assertEqual(list(filas[0].keys()), ["a", "b", "texto,con coma", "d"])
    def test_campos_con_comillas(self):
        texto = 'x,y\n"comilla,\"\"interna\"\"\",2\n'
        filas = parse_csv_robusto(texto)
        self.assertEqual(filas[0]["x"], 'comilla,"interna"')

if __name__ == "__main__":
    unittest.main()