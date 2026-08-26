import subprocess, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def paso(comando, cwd=ROOT):
    print(f"==> {comando}")
    subprocess.run(comando, shell=True, cwd=cwd, check=True)


def hay_cambios():
    out = subprocess.run("git status --porcelain",
                         shell=True, capture_output=True, text=True, cwd=ROOT)
    return bool(out.stdout.strip())


def main():
    paso("python scripts/dncp_contrataciones.py")
    paso("python scripts/generar_datos_web.py")
    paso("python -m unittest discover -s scripts/tests")
    if hay_cambios():
        print("Cambios detectados; en CI se commitea. En local: revisar git status.")
    else:
        print("Sin cambios: dataset y web ya están al día.")


if __name__ == "__main__":
    main()