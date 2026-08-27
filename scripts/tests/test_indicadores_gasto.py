import unittest, os, json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from indicadores_gasto import calcular_indicadores

CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,proveedor,monto,moneda,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,obra1,complete,Obras,open,Municipalidad de Asunción,C1,1000,PYG,,,,x
b,obra2,complete,Obras,open,Municipalidad de Asunción,C1,2000,PYG,,,,x
c,bien1,complete,Bienes,open,Municipalidad de Asunción,C2,500,PYG,,,,x
d,serv1,complete,Servicios,open,Municipalidad de Asunción,C3,300,PYG,,,,x
e,serv2,,Servicios,open,Municipalidad de Asunción,,,PYG,,,,x
"""

class TestIndicadores(unittest.TestCase):
    def test_distribucion_por_categoria(self):
        ind = calcular_indicadores(CSV)
        por_cat = {c["categoria"]: c["monto"] for c in ind["por_categoria"]}
        self.assertEqual(por_cat["Obras"], 3000)
        self.assertEqual(por_cat["Bienes"], 500)
        self.assertEqual(por_cat["Servicios"], 300)
    def test_totales(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["monto_total"], 3800)
        self.assertEqual(ind["procesos"], 5)
        self.assertEqual(ind["proveedores_distintos"], 3)
    def test_top_proveedores_sin_proveedor_debajo(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["top_proveedores"][0]["proveedor"], "C1")
        self.assertEqual(ind["top_proveedores"][0]["monto"], 3000)
        self.assertEqual(ind["procesos_sin_proveedor"], 1)
    def test_categorias_crudas_traducidas(self):
        csv_crudo = CSV.replace("Obras,open", "works,open").replace("Bienes,open", "goods,open").replace("Servicios,open", "services,open")
        ind = calcular_indicadores(csv_crudo)
        cats = {c["categoria"] for c in ind["por_categoria"]}
        self.assertEqual(cats, {"Obras", "Bienes", "Servicios"})

if __name__ == "__main__":
    unittest.main()