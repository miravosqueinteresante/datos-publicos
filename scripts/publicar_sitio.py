import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW = os.path.join(ROOT, "www")
LAB = os.path.join(ROOT, "lab")
SITE = os.path.join(ROOT, "_site")


def ajustar_ruta_lab(texto):
    # en publicación www es la raíz y lab está en /lab: ../www/... -> ../...
    return texto.replace("../www/", "../")


def construir():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    shutil.copytree(WWW, SITE)
    shutil.copytree(LAB, os.path.join(SITE, "lab"))
    for nombre in os.listdir(os.path.join(SITE, "lab")):
        if nombre.endswith(".html"):
            ruta = os.path.join(SITE, "lab", nombre)
            with open(ruta, encoding="utf-8") as f:
                contenido = f.read()
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(ajustar_ruta_lab(contenido))
    cname = os.path.join(SITE, "CNAME")
    if not os.path.exists(cname):
        with open(cname, "w", encoding="utf-8") as f:
            f.write("datospublicos.muchotexto.net")
    return SITE


if __name__ == "__main__":
    print("Sitio construido en:", construir())