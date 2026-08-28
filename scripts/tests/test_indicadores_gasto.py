import unittest, os, json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from indicadores_gasto import calcular_indicadores

CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,valor_estimado,monto_adjudicado,monto_contratado,moneda,n_adjudicaciones,n_proveedores,proveedor,proveedores,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,obra1,complete,Obras,open,Municipalidad de Asuncion,1000,1000,,PYG,1,1,C1,C1,,,,x
b,obra2,complete,Obras,open,Municipalidad de Asuncion,2000,2000,,PYG,1,1,C1,C1,,,,x
c,bien1,complete,Bienes,open,Municipalidad de Asuncion,500,500,,PYG,1,1,C2,C2,,,,x
d,serv1,complete,Servicios,open,Municipalidad de Asuncion,300,300,,PYG,1,1,C3,C3,,,,x
e,serv2,active,Servicios,open,Municipalidad de Asuncion,999,,,PYG,0,0,,,,x
"""

class TestIndicadores(unittest.TestCase):
    def test_distribucion_por_categoria(self):
        ind = calcular_indicadores(CSV)
        por_cat = {c["categoria"]: c["monto"] for c in ind["por_categoria"]}
        self.assertEqual(por_cat["Obras"], 3000)
        self.assertEqual(por_cat["Bienes"], 500)
        self.assertEqual(por_cat["Servicios"], 300)
    def test_totales_separados(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["valor_estimado_total"], 4799)
        self.assertEqual(ind["monto_adjudicado_total"], 3800)
        self.assertEqual(ind["monto_contratado_total"], 0)
        self.assertEqual(ind["procesos"], 5)
        self.assertEqual(ind["procesos_sin_adjudicacion"], 1)
    def test_top_proveedores_usa_adjudicado(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["top_proveedores"][0]["proveedor"], "C1")
        self.assertEqual(ind["top_proveedores"][0]["monto"], 3000)
    def test_pct_sobre_adjudicado(self):
        ind = calcular_indicadores(CSV)
        c1 = next(p for p in ind["top_proveedores"] if p["proveedor"] == "C1")
        self.assertAlmostEqual(c1["pct_del_adjudicado"], 3000/3800*100, places=1)
    def test_categorias_crudas_traducidas(self):
        csv_crudo = CSV.replace("Obras,open", "works,open").replace("Bienes,open", "goods,open").replace("Servicios,open", "services,open")
        ind = calcular_indicadores(csv_crudo)
        cats = {c["categoria"] for c in ind["por_categoria"]}
        self.assertEqual(cats, {"Obras", "Bienes", "Servicios"})

if __name__ == "__main__":
    unittest.main()