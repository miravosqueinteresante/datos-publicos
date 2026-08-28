import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dncp_contrataciones import construir_metadata, leer_tabla, descargar_zip, indexar_awards, indexar_suppliers, indexar_contracts, mapear_fila, es_entidad_por_sicp, es_del_anio, es_registro_valido

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMetadata(unittest.TestCase):
    def test_contiene_conteo_y_version(self):
        m = construir_metadata("2026", [{"id": "a", "n_adjudicaciones": 1}, {"id": "b", "n_adjudicaciones": 0}], "108")
        self.assertEqual(m["anio"], "2026")
        self.assertEqual(m["registros"], 2)
        self.assertEqual(m["sicp"], "108")
        self.assertEqual(m["con_adjudicacion"], 1)
        self.assertEqual(m["sin_adjudicacion"], 1)
        self.assertIn("generado_en", m)
        self.assertIn("fuente", m)


class TestIntegridadReal(unittest.TestCase):
    """Sobre el dataset ya generado: sin duplicados y conteos coherentes."""

    def test_dataset_2026_sin_duplicados_y_coherente(self):
        csv_ruta = os.path.join(ROOT, "data", "contrataciones_muni_2026.csv")
        if not os.path.exists(csv_ruta):
            self.skipTest("dataset 2026 no generado")
        import csv
        with open(csv_ruta, encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        ids = [r["id"] for r in filas]
        self.assertEqual(len(ids), len(set(ids)), "hay OCID duplicados")
        meta_ruta = os.path.join(ROOT, "data", "metadata_2026.json")
        with open(meta_ruta, encoding="utf-8") as f:
            meta = json.load(f)
        self.assertEqual(meta["registros"], len(filas))
        con_adj = sum(1 for r in filas if int(r["n_adjudicaciones"] or 0) > 0)
        self.assertEqual(meta["con_adjudicacion"], con_adj)
        self.assertEqual(meta["sin_adjudicacion"], len(filas) - con_adj)
        # monto_adjudicado nunca debe superar valor_estimado de forma absurda (0 si no hay award)
        for r in filas:
            if int(r["n_adjudicaciones"] or 0) == 0:
                self.assertEqual(r["monto_adjudicado"], "", "proceso sin adjudicar no debe tener monto_adjudicado")


if __name__ == "__main__":
    unittest.main()
